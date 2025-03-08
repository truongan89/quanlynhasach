# bookstore_management/app/models/order.py
from . import db


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)  # 'counter', 'online'
    status = db.Column(db.String(20), default='pending')  # 'pending', 'completed', 'cancelled'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    cancelled_at = db.Column(db.DateTime, nullable=True)

    customer = db.relationship('Account', backref='orders')

    def __repr__(self):
        return f'<Order {self.id}>'