from flask import Blueprint, jsonify, request, make_response
from src.constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from src.database import Relations, Names, db, create_item_models
from src.database import User
from sqlalchemy import func
from flasgger import swag_from
import requests 
import os
from flask_jwt_extended import jwt_required


devices = Blueprint("devices", __name__, url_prefix="/api/v1/devices")

energy_types = {'active_import_energy': 'ACTIVEIMPORTID', 'active_export_energy': 'ACTIVEEXPORTID', 
                'reactive_import_energy': 'REACTIVEIMPORTID', 'reactive_export_energy': 'REACTIVEEXPORTID',  
                'apparent_import_energy': 'APPARENTIMPORTID', 'apparent_export_energy': 'APPARENTEXPORTID'}

OPENHAB_URL=os.environ.get("OPENHAB_URL")
OPENHAB_PORT=os.environ.get("OPENHAB_PORT")
username=os.environ.get("USERNAME")
password=os.environ.get("PASSWORD")


@devices.get('/items')
@jwt_required()
@swag_from('./docs/devices/get_all.yml')
def get_all():
    items = requests.get('https://'+OPENHAB_URL+':'+OPENHAB_PORT+'/rest/items?recursive=false', auth=(username, password))
    if items.ok:
        return items.json(), HTTP_200_OK
    else:
        response = make_response(jsonify({
                'error': 'The service is not available'
            }))
        response.status_code=HTTP_503_SERVICE_UNAVAILABLE
        return response


@devices.get("/items/<itemname>")
@jwt_required()
@swag_from('./docs/devices/item_id.yml')
def item_id(itemname):
    itemname=itemname
    info = requests.get('https://'+OPENHAB_URL+':'+OPENHAB_PORT+'/rest/items/'+itemname+'?recursive=true', auth=(username, password))
    if info.ok:
        return info.json(), HTTP_200_OK
    elif info.status_code == 404:
        response = make_response(jsonify({
                'error': info.json()['error']['message']
            }))
        response.status_code=info.status_code
        return response


@devices.post('/getlastmeasurements')
@jwt_required()
@swag_from('./docs/devices/last_measurement.yml')
def last_measurement():
    ID=request.json.get('id', '')
    measurement=request.json.get('measurement', '')
    start_time=request.json.get('start_time', '')
    end_time=request.json.get('end_time', '')

    if start_time >= end_time:
        response = make_response(jsonify({
            'error': 'The start time is greater than end time'
        }))
        response.status_code=HTTP_400_BAD_REQUEST
    else: 
        names=Names.query.filter_by(ID=ID).first()
        if names:
            if measurement in energy_types:
                relations = Relations.query.filter_by(ID=ID).first()
                col_name = energy_types[measurement]
                
                id = relations.serialize[col_name]

                if id:
                    item = create_item_models('item00'+str(id))
                    #query = item.query.filter(item.TIME >= start_time, item.TIME <= end_time).all()
                    query = item.query.with_entities(func.date_format(item.TIME, '%Y-%m-%d %H'), func.avg(item.VALUE)).filter(item.TIME >= start_time, item.TIME <= end_time).group_by(func.date_format(item.TIME, '%Y-%m-%d %H')).all()
                    response = make_response(jsonify(lastMeasurements=[tuple(row) for row in query]))
                    response.status_code=HTTP_200_OK
                else:
                    response = make_response(jsonify({'error': 'The measurement was not found'}))
                    response.status_code=HTTP_404_NOT_FOUND
            else:
                response = make_response(jsonify({'error': 'That measurement does not exist'}))
                response.status_code=HTTP_404_NOT_FOUND
        else: 
            response = make_response(jsonify({'error': 'Wrong id'}))
            response.status_code = HTTP_400_BAD_REQUEST
    return response