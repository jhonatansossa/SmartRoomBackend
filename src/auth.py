"""Endpoint for authentication"""

import re
from datetime import timedelta
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from flasgger import swag_from
from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN
)
from src.database import User, db, UserTypes

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/register")
@jwt_required()
@swag_from("./docs/auth/register.yml")
def register():
    """Endpoint for registration"""

    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]
    user_type = request.json["user_type"]

    user_id = get_jwt_identity()

    is_admin = User.query.filter_by(id=user_id).with_entities(User.user_type).first()

    if is_admin[0] != 1:
        return (
            jsonify({"error": "You are not allowed to created new users"}),
            HTTP_403_FORBIDDEN,
        )

    if len(password) < 8:
        return jsonify({"error": "Password is too short"}), HTTP_400_BAD_REQUEST
    elif not re.search("[aA-zZ]", password):
        return (
            jsonify({"error": "Password must include at least one character"}),
            HTTP_400_BAD_REQUEST,
        )
    elif not re.search("[0-9]", password):
        return (
            jsonify({"error": "Must include at least one number"}),
            HTTP_400_BAD_REQUEST,
        )

    if len(username) > 20:
        return jsonify({"error": "Username is too long"}), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({"error": "Username is too short"}), HTTP_400_BAD_REQUEST

    if len(email) > 120:
        return jsonify({"error": "Email is too long"}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return (
            jsonify({"error": "Username should be alphanumeric, also no spaces"}),
            HTTP_400_BAD_REQUEST,
        )

    if not isinstance(user_type, str):
        return (
            jsonify({"error": "User type must be an string"}),
            HTTP_400_BAD_REQUEST,
        )

    if not validators.email(email):
        return jsonify({"error": "Email is not valid"}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email is already in use"}), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "Username is already in use"}), HTTP_409_CONFLICT

    user_types = UserTypes.query.filter_by(type=user_type).with_entities(UserTypes.id).first()

    if not user_types:
        return jsonify({"error": "User type not found"}), HTTP_404_NOT_FOUND

    pwd_hash = generate_password_hash(password)

    user = User(username=username, password=pwd_hash, email=email, user_type=user_types[0])
    db.session.add(user)
    db.session.commit()

    return (
        jsonify(
            {"message": "User created", "user": {"username": username, "email": email}}
        ),
        HTTP_201_CREATED,
    )


@auth.post("/login")
@swag_from("./docs/auth/login.yml")
def login():
    """Endpoint for login"""

    email = request.json.get("email", "")
    password = request.json.get("password", "")

    user = User.query.filter_by(email=email).first()
    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(
                identity=user.id, expires_delta=timedelta(days=3)
            )  # expiracion de tokens de 3 dias
            access = create_access_token(
                identity=user.id, expires_delta=timedelta(days=3)
            )  # expiracion de tokens 3 dias

            return (
                jsonify(
                    {
                        "user": {
                            "refresh": refresh,
                            "access": access,
                            "username": user.username,
                            "email": user.email,
                        }
                    }
                ),
                HTTP_200_OK,
            )

    return jsonify({"error": "Wrong Credentials"}), HTTP_401_UNAUTHORIZED


@auth.get("/me")
@jwt_required()
@swag_from("./docs/auth/me.yml")
def me():
    """Endpoint to get user information"""

    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    return jsonify(
        {
            "username": user.username,
            "email": user.email,
            "user_type": user.user_type
        }
    ), HTTP_200_OK


@auth.get("/token/refresh")
@jwt_required(refresh=True)
def refresh_token():
    """Endpoint to refresh access token"""

    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({"access": access}), HTTP_200_OK
