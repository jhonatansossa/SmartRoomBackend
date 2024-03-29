""" Flask APP definition """

import os
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger
from src.auth import auth
from src.database import db
from src.devices import devices, socketio
from src.config.swagger import template, swagger_config


# Application Factory
def create_app(test_config=None):
    """Flask APP creation"""

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    if test_config is None:

        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
            SWAGGER={"title": "DSD Back API", "uiversion": 3},
        )

    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=3)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=3)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(devices)

    Swagger(app, config=swagger_config, template=template)
    socketio.init_app(app, cors_allowed_origins="*", async_mode="eventlet")

    return app
