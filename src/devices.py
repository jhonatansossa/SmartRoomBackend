from flask import Blueprint, jsonify
from src.constants.http_status_codes import HTTP_200_OK
from src.database import Relations, Names, db

devices = Blueprint("devices", __name__, url_prefix="/api/v1/devices")


@devices.get('/alldevices')
def get_all():

    name=Names.query.all()

    return jsonify(devices=[i.serialize for i in name]), HTTP_200_OK