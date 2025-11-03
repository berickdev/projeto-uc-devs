from app import db
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable=False)