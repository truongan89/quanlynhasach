# bookstore_management/app/__init__.py
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager  # Thêm JWT
from .models import db
from config import config
import logging


def create_app(config_name='default'):
    app = Flask(__name__)

    # Cấu hình logging: Ghi log cả vào file và hiển thị trên terminal
    logging.basicConfig(
        level=logging.DEBUG,  # Ghi tất cả log từ DEBUG trở lên
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),  # Ghi log vào file
            logging.StreamHandler()  # Hiển thị log trên terminal
        ]
    )

    logging.debug("Flask app started!")  # Test log khi khởi động ứng dụng

    # Lấy class cấu hình từ dictionary config
    config_class = config.get(config_name, config['default'])
    app.config.from_object(config_class)

    # Khởi tạo SQLAlchemy
    db.init_app(app)

    # Khởi tạo Flask-Migrate
    migrate = Migrate(app, db)

    # Khởi tạo Flask-JWT-Extended
    jwt = JWTManager()
    jwt.init_app(app)

    # Đăng ký blueprint
    from app.routes import register_routes
    register_routes(app)
    return app