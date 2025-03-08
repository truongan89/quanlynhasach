# bookstore_management/app/models/account.py
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)  # Tăng lên 256 ký tự
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'manager', 'staff', 'customer'
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Account {self.username}>'