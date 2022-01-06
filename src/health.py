from flask import Blueprint
from src.constants.http_status_codes import HTTP_200_OK

health = Blueprint("health", __name__, url_prefix="/api/v1/health")

@health.get('/')
def check():
    return 'Good'
