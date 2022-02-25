from flask import Blueprint, jsonify, request, make_response
from src.constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from src.model.database import Relations, Names, db, create_item_models
from src.model.database import User
from sqlalchemy import func

devices = Blueprint("devices", __name__, url_prefix="/api/v1/devices")
energy_types = {'active_import_energy': 'ACTIVEIMPORTID', 'active_export_energy': 'ACTIVEEXPORTID', 
                'reactive_import_energy': 'REACTIVEIMPORTID', 'reactive_export_energy': 'REACTIVEEXPORTID',  
                'apparent_import_energy': 'APPARENTIMPORTID', 'apparent_export_energy': 'APPARENTEXPORTID'}

@devices.get('/alldevices')
def get_all():
    name=Names.query.all()
    return jsonify(devices=[i.serialize for i in name]), HTTP_200_OK

@devices.post('/getlastmeasurements')
def last_mesurement():
    ID=request.json.get('id', '')
    measure=request.json.get('measure', '')
    start_time=request.json.get('start_time', '')
    final_time=request.json.get('final_time', '')

    if start_time >= final_time:
        response = make_response(jsonify({
            'error': 'The start time is greater than final time'
        }))
        response.status_code=HTTP_400_BAD_REQUEST
    else: 
        names=Names.query.filter_by(ID=ID).first()
        if names:
            if measure in energy_types:
                relations = Relations.query.filter_by(ID=ID).first()
                col_name = energy_types[measure]
                
                id = relations.serialize[col_name]

                if id:
                    item = create_item_models('item00'+str(id))
                    query = item.query.filter(item.TIME >= start_time, item.TIME <= final_time).all()
                    response = make_response(jsonify(lastMeasurements=[i.serialize for i in query]))
                    response.status_code=HTTP_200_OK
                else:
                    response = make_response(jsonify({'error': 'The measure was not found'}))
                    response.status_code=HTTP_404_NOT_FOUND
        else: 
            response = make_response(jsonify({'error': 'Wrong id'}))
            response.status_code = HTTP_400_BAD_REQUEST
    return response