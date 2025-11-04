from app import db
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    atendimentos = db.relationship('Atendimento', back_populates='cliente', lazy=True)

    def __repr__(self):
        return f'<Cliente {self.nome}>'
    
class Servico(db.Model):
    __tablename__ = 'servico'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)

    atendimentos = db.relationship('Atendimento', back_populates='servico', lazy=True)

    def __repr__(self):
        return f'<Servico {self.descricao}>'
    
class Atendimento(db.Model):
    __tablename__ = 'atendimento'
    id = db.Column(db.Integer, primary_key=True)
    observacoes = db.Column(db.Text, nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servico.id'), nullable=False)

    cliente = db.relationship('Cliente', back_populates='atendimentos')
    servico = db.relationship('Servico', back_populates='atendimentos')

    def __repr__(self):
        return f'<Atendimento {self.id} - Cliente {self.cliente_id}>'