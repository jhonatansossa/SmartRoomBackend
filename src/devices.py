from flask import Blueprint, jsonify, request, make_response
from src.constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_202_ACCEPTED, HTTP_503_SERVICE_UNAVAILABLE
from src.database import db, ThingItemMeasurement
from sqlalchemy import func
from flasgger import swag_from
import requests 
import os
from flask_jwt_extended import jwt_required
from urllib.parse import quote


devices = Blueprint("devices", __name__, url_prefix="/api/v1/devices")

OPENHAB_URL=os.environ.get("OPENHAB_URL")
OPENHAB_PORT=os.environ.get("OPENHAB_PORT")
username=os.environ.get("USERNAME")
password=os.environ.get("PASSWORD")

@devices.post('/loadmetadata')
@jwt_required()
@swag_from('./docs/devices/get_metadata.yml')
def get_metadata():
    items = requests.get('https://'+OPENHAB_URL+':'+OPENHAB_PORT+'/rest/items?recursive=false', auth=(username, password))
    if items is None:
        response = make_response(jsonify({
                'error': 'The service is not available'
            }))
        response.status_code = HTTP_503_SERVICE_UNAVAILABLE
        return response
    
    items_converted = items.json()

    db.session.query(ThingItemMeasurement).delete()
    db.session.commit()

    for item in items_converted:
        label = item['label'].split('_')
        label_length = len(label)

        if item['label'] == 'Total_Energy_Consumption':
            entry = ThingItemMeasurement(thing_id = 1000, item_id = 1, thing_name = 'Total Energy Consumption', item_name = 'Total_Energy_Consumption_xx_01', measurement_name = 'Total Energy Consumption')
            db.session.add(entry)
            db.session.commit()
            continue

        if label_length == 6:
            thing_name = label[4] + " " + label[0] + " " + label[1]
            measurement_name = label[2] + " " + label[3]
            thing_id = label[4]
        elif label_length == 5:
            thing_name = label[3] + " " + label[0] + " " + label[1]
            measurement_name = label[2]
            thing_id = label[3]
        else:
            thing_name = label[2] + " " + label[0]
            measurement_name = label[1]
            thing_id = label[2]

        item_id = label[-1]
        item_name = item['name']

        entry = ThingItemMeasurement(thing_id = thing_id, item_id = item_id, thing_name = thing_name, item_name = item_name, measurement_name = measurement_name)
        db.session.add(entry)
        db.session.commit()

    return jsonify({
    'message': "Success"
    }), HTTP_200_OK


@devices.get('/relations')
@jwt_required()
@swag_from('./docs/devices/relations.yml')
def get_all_relations():
    result = ThingItemMeasurement.query.all()

    if result is None:
        response = make_response(jsonify({
                'error': 'The service is not available'
            }))
        response.status_code = HTTP_503_SERVICE_UNAVAILABLE
        return response

    output = []

    for row in result:
        output.append({'thing_id': row.thing_id, 'item_id': row.item_id, 'thing_name': row.thing_name, 'item_name': row.item_name, 'measurement_name': row.measurement_name})
    
    return jsonify(output), HTTP_200_OK


@devices.get("/relations/<thingid>")
@jwt_required()
@swag_from('./docs/devices/relations_id.yml')
def get_thing_relations(thingid):
    result = ThingItemMeasurement.query.filter_by(thing_id = thingid).all()

    if result is None:
        response = make_response(jsonify({
                'error': 'The service is not available'
            }))
        response.status_code = HTTP_503_SERVICE_UNAVAILABLE
        return response

    output = []

    for row in result:
        output.append({'thing_id': row.thing_id, 'item_id': row.item_id, 'thing_name': row.thing_name, 'item_name': row.item_name, 'measurement_name': row.measurement_name})
    
    return jsonify(output), HTTP_200_OK


@devices.get('/items')
@jwt_required()
@swag_from('./docs/devices/get_all.yml')
def get_all():
    items = requests.get('https://'+OPENHAB_URL+':'+OPENHAB_PORT+'/rest/items?recursive=false&fields=name,state,label,editable', auth=(username, password))
    if items.ok:
        return items.json(), HTTP_200_OK
    else:
        response = make_response(jsonify({
                'error': 'The service is not available'
            }))
        response.status_code=HTTP_503_SERVICE_UNAVAILABLE
        return response


@devices.get("/items/<thingid>/<itemid>")
@jwt_required()
@swag_from('./docs/devices/item_id.yml')
def thing_item_id(thingid, itemid):
    item = ThingItemMeasurement.query.filter_by(thing_id = thingid, item_id = itemid).first()
    if item is None:
        response = make_response(jsonify({
        'error': 'Item not found'
        }))
        response.status_code=HTTP_404_NOT_FOUND
        return response
    
    info = requests.get('https://'+OPENHAB_URL+':'+OPENHAB_PORT+'/rest/items/'+item.item_name+'?recursive=true', auth=(username, password))

    if info.ok:
        return info.json(), HTTP_200_OK
    
    response = make_response(jsonify({
            'error': info.json()['error']['message']
        }))
    response.status_code=info.status_code
    return response

@devices.get("/items/<itemname>")
@jwt_required()
@swag_from('./docs/devices/get_item.yml')
def item_id(itemname):
    item = ThingItemMeasurement.query.filter_by(item_name = itemname).first()
    if item is None:
        response = make_response(jsonify({
        'error': 'Item not found'
        }))
        response.status_code=HTTP_404_NOT_FOUND
        return response
    
    info = requests.get('https://'+OPENHAB_URL+':'+OPENHAB_PORT+'/rest/items/'+item.item_name+'?recursive=true', auth=(username, password))

    if info.ok:
        return info.json(), HTTP_200_OK
    
    response = make_response(jsonify({
            'error': info.json()['error']['message']
        }))
    response.status_code=info.status_code
    return response

@devices.post("/items/<itemname>/state")
@jwt_required()
@swag_from('./docs/devices/change_state.yml')
def change_state(itemname):
    headers = {'Content-type': 'text/plain'}
    state=request.json.get('state', '')
    itemname=itemname

    print(itemname, state)
    url = f"https://home.myopenhab.org/rest/items/{itemname}/state"
    response = requests.put(url, data=state, headers=headers, auth=(username, password))

    if response.ok:
        return response.content, HTTP_202_ACCEPTED
    else:
        ans = make_response(jsonify({
                'error': response.json()['error']['message']
            }))
        ans.status_code=response.status_code
        return ans


@devices.post('/getlastmeasurements')
@jwt_required()
@swag_from('./docs/devices/last_measurement.yml')
def last_measurement():
    id_thing = request.json.get('thing_id', '')
    measurement = request.json.get('measurement', '')
    start_time = request.json.get('start_time', '')
    end_time = request.json.get('end_time', '')

    if start_time >= end_time:
        response = make_response(jsonify({
            'error': 'The start time is greater than end time'
        }))
        response.status_code=HTTP_400_BAD_REQUEST
        return response
    
    entry = ThingItemMeasurement.query.filter_by(thing_id = id_thing, measurement_name = measurement).first()

    if entry is None:
        response = make_response(jsonify({
            'error': "Measurement not found"
        }))
        response.status_code=HTTP_404_NOT_FOUND
        return response
    
    item_name = entry.item_name
    start_time_formatted = quote(start_time.replace(" ", "-"))
    end_time_formatted = quote(end_time.replace(" ", "-"))

    response = requests.get('https://'+OPENHAB_URL+':'+OPENHAB_PORT+'/rest/persistence/items/'+item_name+'?starttime='+start_time_formatted+'&endtime='+end_time_formatted, auth=(username, password))

    if response.ok:
        return jsonify(response.json()), HTTP_200_OK

    ans = make_response(jsonify({
            'error': response.json()['error']['message']
        }))
    ans.status_code=response.status_code
    return ans