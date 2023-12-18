import os
import time
import requests
import threading
from src.database import ThingItemMeasurement
from flask import jsonify, make_response
from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_503_SERVICE_UNAVAILABLE,
)
from datetime import datetime

OPENHAB_URL = os.environ.get("OPENHAB_URL")
OPENHAB_PORT = os.environ.get("OPENHAB_PORT")
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")

current_turnoff_thread = None
current_dooralarm_thread = None
terminate_turnoff_flag = threading.Event()
terminate_dooralarm_flag = threading.Event()

def check_if_empty_or_open(start_time, end_time, thing_id, item_id):

    itemname = (
        ThingItemMeasurement.query.filter_by(thing_id=thing_id, item_id=item_id)
        .with_entities(ThingItemMeasurement.item_name).first()
    )

    try:
        persisted_url = f"https://{OPENHAB_URL}:{OPENHAB_PORT}/rest/persistence/items/{itemname[0]}?starttime={start_time}&endtime={end_time}"
        live_url = f"https://{OPENHAB_URL}:{OPENHAB_PORT}/rest/items/{itemname[0]}/state"
    except Exception as e: 
        print(f"There is not an item for the number of people: {str(e)}")

    persisted_response = requests.get(persisted_url, auth=(username, password))
    live_response = requests.get(live_url, auth=(username, password))

    states = [float(x["state"]) for x in persisted_response.json()["data"]] + [live_response.json()]

    empty_or_open = len([x for x in states if int(x) != 0]) == 0

    return empty_or_open


def turn_off_devices(app_context, seconds, socketio):
    global terminate_turnoff_flag

    app_context.push()

    start_time = datetime.now()
    for _ in range(seconds):
        if terminate_turnoff_flag.is_set():
            return
        time.sleep(1)

    end_time = datetime.now()

    start_time, end_time = start_time.strftime(
        "%Y-%m-%dT%H:%M:%S.%f"
    ), end_time.strftime("%Y-%m-%dT%H:%M:%S.%f")

    is_empty = check_if_empty_or_open(start_time, end_time, 1000, 5)

    if not is_empty:
        return

    devices_count_off = 0

    try:
        devices_to_turn_off = ThingItemMeasurement.query.filter_by(auto_switchoff=1).all()
    except Exception as e:
        print(f"Error getting devices: {str(e)}, {HTTP_503_SERVICE_UNAVAILABLE}")
        return

    for device in devices_to_turn_off:
        item_name = device.item_name

        headers = {"Content-type": "text/plain"}
        url = f"https://{OPENHAB_URL}:{OPENHAB_PORT}/rest/items/{item_name}"

        response = requests.post(url, data="OFF", headers=headers, auth=(username, password))

        if response.ok:
            devices_count_off += 1
        else:
            error_message = response.json().get('error', {}).get('message', 'Unknown error')
            print(f"Error turning off device {item_name}: {error_message}, {HTTP_404_NOT_FOUND}")
            return

    socketio.emit('devices-off', {'data': 'The devices have been automatically turned off'})

    return


def trigger_door_alarm(app_context, minutes, socketio):
    global terminate_dooralarm_flag

    app_context.push()

    seconds = minutes * 60

    start_time = datetime.now()
    for _ in range(seconds):
        if terminate_dooralarm_flag.is_set():
            return
        time.sleep(1)

    end_time = datetime.now()

    start_time, end_time = start_time.strftime(
        "%Y-%m-%dT%H:%M:%S.%f"
    ), end_time.strftime("%Y-%m-%dT%H:%M:%S.%f")

    is_empty = check_if_empty_or_open(start_time, end_time, 1000, 5)
    is_open = check_if_empty_or_open(start_time, end_time, 12, 1)

    if is_empty and is_open:
        socketio.emit('door-alarm', {'data': 'The door has been opened for more than 5 minutes'})

    return
