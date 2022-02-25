from flask import Flask
import os
from src.services.auth import auth
from src.services.bookmarks import bookmarks
from src.model.database import db
from src.services.devices import devices
from flask_jwt_extended import JWTManager
from flask_cors import CORS

#Application Factory
def create_app(test_config=None):

    app=Flask(__name__,
    instance_relative_config=True)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    if test_config is None:

        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY")
        )

    else:
        app.config.from_mapping(test_config)


    db.app=app
    db.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    app.register_blueprint(devices)

    return app
