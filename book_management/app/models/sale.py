# bookstore_management/app/models/sale.py
from . import db


class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    sold_by = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    sold_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    book = db.relationship('Book', backref='sales')
    seller = db.relationship('Account', backref='sales')

    def __repr__(self):
        return f'<Sale {self.id}>'