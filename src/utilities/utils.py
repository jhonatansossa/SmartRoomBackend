import os
import time
import requests
from src.database import ThingItemMeasurement
from flask import jsonify, make_response
from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_503_SERVICE_UNAVAILABLE,
)
from datetime import datetime, timedelta

OPENHAB_URL = os.environ.get("OPENHAB_URL")
OPENHAB_PORT = os.environ.get("OPENHAB_PORT")
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")

def check_if_turn_off(app_context, seconds, socketio):
    app_context.push()
    
    start_time = datetime.now()
    time.sleep(seconds)
    end_time = datetime.now()

    start_time, end_time = start_time.strftime(
        "%Y-%m-%dT%H:%M:%S.%f"
    ), end_time.strftime("%Y-%m-%dT%H:%M:%S.%f")

    number_people_itemname = (
        ThingItemMeasurement.query.filter_by(thing_id=1000, item_id=5)
        .with_entities(ThingItemMeasurement.item_name).first()
    )

    try:
        persisted_url = f"https://{OPENHAB_URL}:{OPENHAB_PORT}/rest/persistence/items/{number_people_itemname[0]}?starttime={start_time}&endtime={end_time}"
        live_url = f"https://{OPENHAB_URL}:{OPENHAB_PORT}/rest/items/{number_people_itemname[0]}/state"
    except Exception as e: 
        print(f"There is not an item for the number of people: {str(e)}")

    persisted_response = requests.get(persisted_url, auth=(username, password))
    live_response = requests.get(live_url, auth=(username, password))

    states = [float(x["state"]) for x in persisted_response.json()["data"]] + [live_response.json()]

    execute_turn_off = len([x for x in states if int(x) != 0]) == 0


    if execute_turn_off:
        turn_off_devices(socketio)

    return execute_turn_off


def turn_off_devices(socketio):
    devices_count_off = 0

    try:
        devices_to_turn_off = ThingItemMeasurement.query.filter_by(auto_switchoff=1).all()
    except Exception as e:
        print(f"Error getting devices: {str(e)}")
        response = make_response(jsonify({"error": "The service is not available"}))
        response.status_code = HTTP_503_SERVICE_UNAVAILABLE
        return response

    for device in devices_to_turn_off:
        item_name = device.item_name

        headers = {"Content-type": "text/plain"}
        url = f"https://{OPENHAB_URL}:{OPENHAB_PORT}/rest/items/{item_name}"

        response = requests.post(url, data="OFF", headers=headers, auth=(username, password))

        if response.ok:
            devices_count_off += 1
        else:
            error_message = response.json().get('error', {}).get('message', 'Unknown error')
            print(f"Error turning off device {item_name}: {error_message}")
            response = make_response(jsonify({"error": f"Failed to turn off device {item_name}: {error_message}"}))
            response.status_code = HTTP_404_NOT_FOUND
            return response

    socketio.emit('devices-off', {'data': 'The devices have been automatically turned off'})

    return jsonify(
        {
            "devices_count_off": devices_count_off,
            "message": "Devices turned off successfully",
        }
    ), HTTP_200_OK
