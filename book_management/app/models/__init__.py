# bookstore_management/app/models/__init__.py
from flask_sqlalchemy import SQLAlchemy

# Khởi tạo đối tượng SQLAlchemy
db = SQLAlchemy()

# Import tất cả models
from .account import Account
from .book import Book
from .book_import import BookImport
from .cate import Cate
from .log import Log
from .order import Order
from .order_detail import OrderDetail
from .sale import Sale
from .setting import Setting