# app/routes/main.py
from flask import Blueprint

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return "Chào mừng bạn! <a href='/login'>Đăng nhập</a>"