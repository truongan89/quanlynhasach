# bookstore_management/app/models/book_import.py
from . import db


class BookImport(db.Model):
    __tablename__ = 'book_imports'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    imported_by = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    imported_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    book = db.relationship('Book', backref='imports')
    importer = db.relationship('Account', backref='book_imports')

    def __repr__(self):
        return f'<BookImport {self.id}>'