# app/models.py

from . import db


class PDFFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    upload_date = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )

    def __init__(self, filename: str):
        self.filename = filename

    def __repr__(self):
        return f"PDFFile('{self.filename}', '{self.upload_date}')"
