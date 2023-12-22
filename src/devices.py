import threading
from flask import Blueprint, jsonify, request, make_response, current_app
from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_202_ACCEPTED,
    HTTP_503_SERVICE_UNAVAILABLE,
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from src.utilities.utils import (
    turn_off_devices,
    trigger_door_alarm,
    current_turnoff_thread,
    current_dooralarm_thread,
    terminate_turnoff_flag,
    terminate_dooralarm_flag,
)
from src.database import db, ThingItemMeasurement, RoomStatus, AlertTimers,NewItemNames
from flasgger import swag_from
import requests
import os
from flask_jwt_extended import jwt_required
from flask_socketio import SocketIO
from urllib.parse import quote
from datetime import datetime

socketio = SocketIO()
devices = Blueprint("devices", __name__, url_prefix="/api/v1/devices")

OPENHAB_URL = os.environ.get("OPENHAB_URL")
OPENHAB_PORT = os.environ.get("OPENHAB_PORT")
OPENHAB_TOKEN = os.environ.get("OPENHAB_TOKEN")
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")


@devices.post("/loadmetadata")
@jwt_required()
@swag_from("./docs/devices/get_metadata.yml")
def get_metadata():
    auto_switchoff_items = request.json.get("items", "")

    items = requests.get(
        "https://" + OPENHAB_URL + ":" + OPENHAB_PORT + "/rest/items?recursive=false",
        auth=(username, password),
    )
    if items is None:
        response = make_response(jsonify({"error": "The service is not available"}))
        response.status_code = HTTP_503_SERVICE_UNAVAILABLE
        return response

    items_converted = items.json()

    try:
        ThingItemMeasurement.__table__.drop(db.engine)
    except Exception as e:
        print(e)

    db.create_all()
    db.session.commit()

    for item in items_converted:
        label = item["label"].split("_")
        item_type = item["type"]

        if item["name"] in auto_switchoff_items:
            auto_switchoff = True
        else:
            auto_switchoff = False

        thing_id = label[-2]
        item_id = label[-1]
        measurement_name = label[-3]
        thing_name = " ".join([thing_id] + label[:-3])
        item_name = item["name"]

        entry = ThingItemMeasurement(
            thing_id=thing_id,
            item_id=item_id,
            thing_name=thing_name,
            item_type=item_type,
            item_name=item_name,
            measurement_name=measurement_name,
            auto_switchoff=auto_switchoff,
        )
        db.session.add(entry)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    return jsonify({"message": "Success"}), HTTP_200_OK


@devices.get("/relations")
@jwt_required()
@swag_from("./docs/devices/relations.yml")
def get_all_relations():
    result = ThingItemMeasurement.query.all()

    if result is None:
        response = make_response(jsonify({"error": "The service is not available"}))
        response.status_code = HTTP_503_SERVICE_UNAVAILABLE
        return response

    output = []

    for row in result:
        output.append(
            {
                "thing_id": row.thing_id,
                "item_id": row.item_id,
                "thing_name": row.thing_name,
                "item_name": row.item_name,
                "item_type": row.item_type,
                "measurement_name": row.measurement_name,
            }
        )

    return jsonify(output), HTTP_200_OK


@devices.get("/relations/<thingid>")
@jwt_required()
@swag_from("./docs/devices/relations_id.yml")
def get_thing_relations(thingid):
    result = ThingItemMeasurement.query.filter_by(thing_id=thingid).all()

    if result is None:
        response = make_response(jsonify({"error": "The service is not available"}))
        response.status_code = HTTP_503_SERVICE_UNAVAILABLE
        return response

    output = []

    for row in result:
        output.append(
            {
                "thing_id": row.thing_id,
                "item_id": row.item_id,
                "thing_name": row.thing_name,
                "item_name": row.item_name,
                "measurement_name": row.measurement_name,
            }
        )

    return jsonify(output), HTTP_200_OK


@devices.get("/items")
@jwt_required()
@swag_from("./docs/devices/get_all.yml")
def get_all():
    items = requests.get(
        "https://"
        + OPENHAB_URL
        + ":"
        + OPENHAB_PORT
        + "/rest/items?recursive=false&fields=name,state,label,editable,type",
        auth=(username, password),
    )
    if items.ok:
        return items.json(), HTTP_200_OK
    else:
        response = make_response(jsonify({"error": "The service is not available"}))
        response.status_code = HTTP_503_SERVICE_UNAVAILABLE
        return response


@devices.get("/items/<thingid>/<itemid>")
@jwt_required()
@swag_from("./docs/devices/item_id.yml")
def thing_item_id(thingid, itemid):
    item = ThingItemMeasurement.query.filter_by(
        thing_id=thingid, item_id=itemid
    ).first()
    if item is None:
        response = make_response(jsonify({"error": "Item not found"}))
        response.status_code = HTTP_404_NOT_FOUND
        return response

    info = requests.get(
        "https://"
        + OPENHAB_URL
        + ":"
        + OPENHAB_PORT
        + "/rest/items/"
        + item.item_name
        + "?recursive=true",
        auth=(username, password),
    )

    if info.ok:
        return info.json(), HTTP_200_OK

    response = make_response(jsonify({"error": info.json()["error"]["message"]}))
    response.status_code = info.status_code
    return response


@devices.get("/items/<itemname>")
@jwt_required()
@swag_from("./docs/devices/get_item.yml")
def item_id(itemname):
    item = ThingItemMeasurement.query.filter_by(item_name=itemname).first()
    if item is None:
        response = make_response(jsonify({"error": "Item not found"}))
        response.status_code = HTTP_404_NOT_FOUND
        return response

    info = requests.get(
        "https://"
        + OPENHAB_URL
        + ":"
        + OPENHAB_PORT
        + "/rest/items/"
        + item.item_name
        + "?recursive=true",
        auth=(username, password),
    )

    if info.ok:
        return info.json(), HTTP_200_OK

    response = make_response(jsonify({"error": info.json()["error"]["message"]}))
    response.status_code = info.status_code
    return response


@devices.post("/items/<thingid>/<itemid>/state")
@jwt_required()
@swag_from("./docs/devices/change_state.yml")
def change_state(thingid, itemid):

    item = ThingItemMeasurement.query.filter_by(
        thing_id=thingid, item_id=itemid
    ).first()
    if item is None:
        response = make_response(jsonify({"error": "Item not found"}))
        response.status_code = HTTP_404_NOT_FOUND
        return response

    if item.item_type != "Switch":
        response = make_response(
            jsonify({"error": "The state of this item cannot be changed."})
        )
        response.status_code = HTTP_400_BAD_REQUEST
        return response

    headers = {"Content-type": "text/plain"}
    state = request.json.get("state", "")
    itemname = item.item_name

    url = f"https://{OPENHAB_URL}:{OPENHAB_PORT}/rest/items/{itemname}"
    response = requests.post(
        url, data=state, headers=headers, auth=(username, password)
    )

    if response.ok:
        return response.content, HTTP_202_ACCEPTED
    else:
        ans = make_response(jsonify({"error": response.json()["error"]["message"]}))
        ans.status_code = response.status_code
        return ans


@devices.post("/getlastmeasurements")
@jwt_required()
@swag_from("./docs/devices/last_measurement.yml")
def last_measurement():
    thing_id = request.json.get("thing_id", "")
    measurement = request.json.get("measurement", "")
    start_time = request.json.get("start_time", "")
    end_time = request.json.get("end_time", "")

    start_time, end_time = datetime.strptime(
        start_time, "%Y-%m-%d %H:%M:%S"
    ), datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    start_time, end_time = start_time.strftime(
        "%Y-%m-%dT%H:%M:%S.%fZ"
    ), end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    if start_time >= end_time:
        response = make_response(
            jsonify({"error": "The start time is greater than end time"})
        )
        response.status_code = HTTP_400_BAD_REQUEST
        return response

    entry = ThingItemMeasurement.query.filter_by(
        thing_id=thing_id, measurement_name=measurement
    ).first()

    if entry is None:
        response = make_response(jsonify({"error": "Measurement or thing not found"}))
        response.status_code = HTTP_404_NOT_FOUND
        return response

    item_name = entry.item_name
    start_time_formatted = quote(start_time.replace(" ", "-"))
    end_time_formatted = quote(end_time.replace(" ", "-"))

    response = requests.get(
        "https://"
        + OPENHAB_URL
        + ":"
        + OPENHAB_PORT
        + "/rest/persistence/items/"
        + item_name
        + "?starttime="
        + start_time_formatted
        + "&endtime="
        + end_time_formatted,
        auth=(username, password),
    )

    if response.ok:
        return jsonify(response.json()), HTTP_200_OK

    ans = make_response(jsonify({"error": response.json()["error"]["message"]}))
    ans.status_code = response.status_code
    return ans


@devices.get("/energy_consumption")
@jwt_required()
@swag_from("./docs/devices/energy_consumption.yml")
def get_energy_consumption():
    total_energy = 0
    devices_count = 0
    switch_count = 0
    try:
        switches = (
            ThingItemMeasurement.query.filter_by(item_type="Switch")
            .filter(~ThingItemMeasurement.item_name.ilike("%Sensor%"))
            .with_entities(ThingItemMeasurement.item_name)
            .all()
        )
    except:
        response = make_response(jsonify({"error": "The service is not available"}))
        response.status_code = HTTP_503_SERVICE_UNAVAILABLE
        return response

    switch_count = len(switches)

    response = requests.get(
        "https://"
        + OPENHAB_URL
        + ":"
        + OPENHAB_PORT
        + "/rest/items?recursive=false&fields=name,state",
        auth=(username, password),
    )

    if not response.ok:
        ans = make_response(jsonify({"error": response.json()["error"]["message"]}))
        ans.status_code = response.status_code
        return ans

    for switch in switches:
        item_name = switch.item_name

        state = list(
            filter(
                lambda x: (x["name"] == item_name and x["state"] == "ON"),
                response.json(),
            )
        )

        if len(state) != 0 and state[0]["state"] == "ON":
            devices_count += 1
    try:
        devices = (
            ThingItemMeasurement.query.filter_by(measurement_name="meterwatts")
            .with_entities(ThingItemMeasurement.item_name)
            .all()
        )
    except:
        response = make_response(jsonify({"error": "The service is not available"}))
        response.status_code = HTTP_503_SERVICE_UNAVAILABLE
        return response

    for device in devices:
        item_name = device.item_name

        watts = list(filter(lambda x: (x["name"] == item_name), response.json()))

        if len(watts) != 0:
            energy_value = float(watts[0]["state"])
            total_energy += energy_value

    if devices_count != 0:
        average_energy = total_energy / devices_count
    else:
        average_energy = 0

    return (
        jsonify(
            {
                "total_energy": total_energy,
                "average_energy": average_energy,
                "devices_count": devices_count,
                "switch_count": switch_count,
            }
        ),
        HTTP_200_OK,
    )


@devices.get("/roomstatus")
@jwt_required()
@swag_from("./docs/devices/get_room_status.yml")
def get_room_status():
    try:
        response = requests.get(
            "https://"
            + OPENHAB_URL
            + ":"
            + OPENHAB_PORT
            + "/rest/items/Number_people_detection_1000_05",
            auth=(username, password),
        )

        if not response.ok:
            ans = make_response(jsonify({"error": response.json()["error"]["message"]}))
            ans.status_code = response.status_code
            return ans

        amount = int(response.json()["state"])
        if amount > 0:
            people_detection = True
        else:
            people_detection = False

        try:
            entry = RoomStatus(status=people_detection, amount=amount)
            db.session.add(entry)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.create_all()

        db.session.add(entry)
        db.session.commit()

    except Exception as e:
        print(e)
        response = make_response(jsonify({"error": "The service is not available"}))
        response.status_code = HTTP_503_SERVICE_UNAVAILABLE
        return response

    return jsonify({"detection": people_detection, "amount": amount}), HTTP_200_OK


@devices.put("/automaticturnoffdevices")
def turn_off_devices_with_auto():
    global current_turnoff_thread, terminate_turnoff_flag

    if request.headers.get("X-Service-Token") == OPENHAB_TOKEN:
        
        # Get the timer for the alert to turn off the devices (id=1 in table alert_timers)
        timer = (
            AlertTimers.query.filter_by(id=1)
            .with_entities(AlertTimers.timer_value, AlertTimers.timer_units)
            .first()
        )

        if timer.timer_units == "minutes":
            seconds = timer.timer_value * 60
        else:
            seconds = timer.timer_value

        try:
            terminate_turnoff_flag.set()

            if current_turnoff_thread and current_turnoff_thread.is_alive():
                current_turnoff_thread.join()
                print(f"Process {current_turnoff_thread} killed")

            terminate_turnoff_flag.clear()

            current_turnoff_thread = threading.Thread(
                target=turn_off_devices,
                args=(current_app.app_context(), seconds, socketio),
                daemon=True,
            )
            current_turnoff_thread.start()

            response = make_response(
                jsonify({"message": "The request will be processed"})
            )
            response.status_code = HTTP_200_OK
        except Exception as e:
            response = make_response(
                jsonify(
                    {"message": f"The service is not available. Associated error: {e}"}
                )
            )
            response.status_code = HTTP_503_SERVICE_UNAVAILABLE
    else:
        response = make_response(jsonify({"message": "Unauthorized"}))
        response.status_code = HTTP_401_UNAUTHORIZED

    return response


@devices.put("/dooralarm")
def door_alarm():
    global current_dooralarm_thread, terminate_dooralarm_flag

    if request.headers.get("X-Service-Token") == OPENHAB_TOKEN:

        # Get the timer of the alert when the door was left open (id=0 in table alert_timers)
        timer = (
            AlertTimers.query.filter_by(id=0)
            .with_entities(AlertTimers.timer_value, AlertTimers.timer_units)
            .first()
        )

        if timer.timer_units == "minutes":
            seconds = timer.timer_value * 60
        else:
            seconds = timer.timer_value

        try:
            terminate_dooralarm_flag.set()

            if current_dooralarm_thread and current_dooralarm_thread.is_alive():
                current_dooralarm_thread.join()
                print(f"Process {current_dooralarm_thread} killed")

            terminate_dooralarm_flag.clear()

            current_dooralarm_thread = threading.Thread(
                target=trigger_door_alarm,
                args=(current_app.app_context(), seconds, socketio),
                daemon=True,
            )
            current_dooralarm_thread.start()

            response = make_response(
                jsonify({"message": "The request will be processed"})
            )
            response.status_code = HTTP_200_OK
        except Exception as e:
            response = make_response(
                jsonify(
                    {"message": f"The service is not available. Associated error: {e}"}
                )
            )
            response.status_code = HTTP_503_SERVICE_UNAVAILABLE
    else:
        response = make_response(jsonify({"message": "Unauthorized"}))
        response.status_code = HTTP_401_UNAUTHORIZED

    return response


@devices.get("/get_alarm_timers")
@jwt_required()
@swag_from("./docs/devices/get_alarm_timers.yml")
def get_alarm_timers():

    result = AlertTimers.query.all()

    if result is None:
        response = make_response(
            jsonify({"error": "It was not possible to retrieve any timer"})
        )
        response.status_code = HTTP_500_INTERNAL_SERVER_ERROR
        return response

    output = []

    for row in result:
        output.append(
            {
                "id": row.id,
                "alert_name": row.alert_name,
                "timer_value": row.timer_value,
                "timer_units": row.timer_units,
            }
        )

    return jsonify(output), HTTP_200_OK


@devices.put("/set_alarm_timers")
@jwt_required()
@swag_from("./docs/devices/set_alarm_timers.yml")
def set_alarm_timers():

    alert_id = request.json.get("id", "")
    timer_units = request.json.get("timer_units", "")
    timer_value = request.json.get("timer_value", "")

    if alert_id == "" or timer_units == "" or timer_value == "":
        return (
            jsonify({"error": "Please provide alert_id, timer_units and timer_value"}),
            HTTP_400_BAD_REQUEST,
        )

    if timer_units not in ["seconds", "minutes"]:
        return (
            jsonify({"error": "Timer units is neither seconds nor minutes"}),
            HTTP_400_BAD_REQUEST,
        )

    if not isinstance(timer_value, int):
        return (
            jsonify({"error": "The timer_value must be an integer"}),
            HTTP_400_BAD_REQUEST,
        )

    if timer_value < 0:
        return (
            jsonify({"error": "Timer value cannot be less than zero"}),
            HTTP_400_BAD_REQUEST,
        )

    if not isinstance(alert_id, int):
        return (
            jsonify({"error": "The alert id must be an integer"}),
            HTTP_400_BAD_REQUEST,
        )

    ids = AlertTimers.query.with_entities(AlertTimers.id).all()

    if alert_id not in [id_[0] for id_ in ids]:
        return jsonify({"error": "Alarm id not found"}), HTTP_404_NOT_FOUND

    try:
        AlertTimers.query.filter_by(id=alert_id).update(
            {"timer_units": timer_units, "timer_value": timer_value}
        )
        db.session.commit()
    except Exception as e:
        return (
            jsonify({"error": f"It was not possible to update the timer. Reason: {e}"}),
            HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return {"result": "The timer has been successfully updated"}, HTTP_200_OK

@devices.put("/new_item_names")
@jwt_required()
@swag_from("./docs/devices/new_item_name.yml")
def add_new_item_name():
    thing_id = request.json.get("thing_id", "")
    item_id = request.json.get("item_id", "")
    item_name = request.json.get("item_name", "")
    new_item_name = request.json.get("new_item_name", "")
    if not thing_id or not item_id or not item_name or not new_item_name:
        response = make_response(
            jsonify({"error": "Please provide thing_id, item_id, item_name, and new_item_name"}),
        )
        response.status_code = HTTP_400_BAD_REQUEST
        return response  
    if not ThingItemMeasurement.query.filter_by(thing_id=thing_id, item_id=item_id).first():
        response = make_response(
            jsonify({"error": "Provided thing_id and item_id do not exist in the thing_item_measurement table"}),
        )
        response.status_code = HTTP_404_NOT_FOUND
        return response
    try:        
        existing_entry = NewItemNames.query.filter_by(thing_id=thing_id, item_id=item_id).first()
        if existing_entry:
            
            
            existing_entry.new_item_name = new_item_name
        else:       
            new_item_name_entry = NewItemNames(
                thing_id=thing_id,
                item_id=item_id,
                item_name=item_name,
                new_item_name=new_item_name
            )
            db.session.add(new_item_name_entry)
        db.session.commit()
    except IntegrityError as e:
        
        db.session.rollback()
        response = make_response(
            jsonify({"error": f"Failed to add/update new item name. Reason: {e}"}),
        )
        response.status_code = HTTP_500_INTERNAL_SERVER_ERROR
        return response
    except Exception as e:
        response = make_response(
            jsonify({"error": f"Failed to add/update new item name. Reason: {e}"}),
        )
        response.status_code = HTTP_500_INTERNAL_SERVER_ERROR
        return response

    return jsonify({"message": "New item name added/updated successfully"}), HTTP_200_OK


@devices.get("/retrieve_new_item_names")
@jwt_required()
@swag_from("./docs/devices/retrieve_new_item_names.yml")
def retrieve_new_item_names():
    try:
        new_item_names = NewItemNames.query.all()
        item_names_data = [{"thing_id": entry.thing_id, "item_id": entry.item_id, "item_name": entry.item_name, "new_item_name": entry.new_item_name} for entry in new_item_names]
    except Exception:
        response = make_response(jsonify({"error": "Failed to retrieve data from new_item_names table"}))
        response.status_code = HTTP_500_INTERNAL_SERVER_ERROR
        return response

    return jsonify({"new_item_names": item_names_data}), HTTP_200_OK