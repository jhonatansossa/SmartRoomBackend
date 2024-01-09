import os
import time
import requests
import threading
from src.database import ThingItemMeasurement
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

door_status = {"CLOSED": 1, "OPEN": 0}


def check_if_empty_or_open(start_time, end_time, thing_id, item_id):

    itemname = (
        ThingItemMeasurement.query.filter_by(thing_id=thing_id, item_id=item_id)
        .with_entities(ThingItemMeasurement.item_name)
        .first()
    )

    try:
        persisted_url = f"https://{OPENHAB_URL}:{OPENHAB_PORT}/rest/persistence/items/{itemname[0]}?starttime={start_time}&endtime={end_time}"
        live_url = (
            f"https://{OPENHAB_URL}:{OPENHAB_PORT}/rest/items/{itemname[0]}/state"
        )
    except Exception as e:
        print(
            f"There is not an item for this combination if thing_id and item_id: {str(e)}"
        )

    persisted_response = requests.get(persisted_url, auth=(username, password))
    live_response = requests.get(live_url, auth=(username, password))

    persisted_response = [
        door_status[x["state"]] if (x["state"] in door_status) else float(x["state"])
        for x in persisted_response.json()["data"]
    ]
    live_response = [
        door_status[live_response.content.decode()]
        if live_response.content.decode() in door_status
        else float(live_response.content.decode())
    ]

    states = persisted_response + live_response

    empty_or_open = len([x for x in states if int(x) != 0]) == 0

    return empty_or_open


def turn_off_devices(app_context, seconds, socketio):
    global terminate_turnoff_flag

    app_context.push()

    print(f"Turn off Devices Log: Trigger timer")

    start_time = datetime.now()
    for _ in range(seconds):
        if terminate_turnoff_flag.is_set():
            print(f"Turn off Devices Log: Thread terminated")
            return
        time.sleep(1)

    end_time = datetime.now()

    start_time, end_time = start_time.strftime(
        "%Y-%m-%dT%H:%M:%S.%f"
    ), end_time.strftime("%Y-%m-%dT%H:%M:%S.%f")

    # Check if the room is empty. The parameters are for the item with thing_id=1000 and item_id=5 (People counter)
    is_empty = check_if_empty_or_open(start_time, end_time, 1000, 5)

    print(f"Turn off Devices Log: is empty {is_empty}")

    if not is_empty:
        return

    devices_count_off = 0

    try:
        devices_to_turn_off = ThingItemMeasurement.query.filter_by(
            auto_switchoff=1
        ).all()
    except Exception as e:
        print(f"Error getting devices: {str(e)}, {HTTP_503_SERVICE_UNAVAILABLE}")
        return

    for device in devices_to_turn_off:
        item_name = device.item_name

        headers = {"Content-type": "text/plain"}
        url = f"https://{OPENHAB_URL}:{OPENHAB_PORT}/rest/items/{item_name}"

        response = requests.post(
            url, data="OFF", headers=headers, auth=(username, password)
        )

        if response.ok:
            devices_count_off += 1
        else:
            error_message = (
                response.json().get("error", {}).get("message", "Unknown error")
            )
            print(
                f"Error turning off device {item_name}: {error_message}, {HTTP_404_NOT_FOUND}"
            )
            return

    socketio.emit(
        "devices-off", {"data": "The devices have been automatically turned off"}
    )
    print(f"Turn off Devices Log: Alarm emited")

    return


def trigger_door_alarm(app_context, seconds, socketio):
    global terminate_dooralarm_flag

    app_context.push()

    print(f"Door Alarm Log: Trigger timer")

    start_time = datetime.now()
    for _ in range(seconds):
        if terminate_dooralarm_flag.is_set():
            print(f"Door Alarm Log: Thread terminated")
            return
        time.sleep(1)

    end_time = datetime.now()

    start_time, end_time = start_time.strftime(
        "%Y-%m-%dT%H:%M:%S.%f"
    ), end_time.strftime("%Y-%m-%dT%H:%M:%S.%f")

    # # Check if the door is open. The parameters are for the item with thing_id=12 and item_id=1 (Door contact sensor)
    is_open = check_if_empty_or_open(start_time, end_time, 12, 1)

    # Check if the room is empty. The parameters are for the item with thing_id=1000 and item_id=5 (People counter)
    is_empty = check_if_empty_or_open(start_time, end_time, 1000, 5)

    print(f"Door Alarm Log: is open {is_open} and is empty {is_empty}")

    if is_empty and is_open:
        socketio.emit(
            "door-alarm", {"data": "The door has been opened for more than 5 minutes"}
        )
        print(f"Door Alarm Log: Alarm emited")

    return
