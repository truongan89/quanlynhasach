# book_management/app/routes/auth.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime
from config import Config

auth_bp = Blueprint("auth", __name__)

users = {"admin": "password123"}  # Danh sách user giả lập


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if users.get(username) == password:
        access_token = create_access_token(identity=username)
        print(f"Generated JWT Token: {access_token}")  # ✅ In token ra console
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Đăng nhập thất bại!"}), 401


@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    print(f"Checking JWT with secret: {Config.JWT_SECRET_KEY}")
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user)
