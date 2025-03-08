# bookstore_management/app/models/setting.py
from . import db


class Setting(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)  # 'min_import', 'min_stock', 'cancel_time'
    value = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Setting {self.key}>'