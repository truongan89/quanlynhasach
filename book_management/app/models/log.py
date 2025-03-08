# bookstore_management/app/models/log.py
from . import db


class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)  # 'import', 'sale', 'order', 'setting_change', 'security'
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('Account', backref='logs')

    def __repr__(self):
        return f'<Log {self.action}>'