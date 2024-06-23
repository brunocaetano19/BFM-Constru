from . import db

class Estoque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade_disponivel = db.Column(db.Integer, nullable=False)
    quantidade_reservada = db.Column(db.Integer, nullable=False)

class OrdemServico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='em andamento')
    itens = db.relationship('ItemOrdemServico', back_populates='ordem', cascade='all, delete-orphan')

class ItemOrdemServico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ordem_id = db.Column(db.Integer, db.ForeignKey('ordem_servico.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('estoque.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    ordem = db.relationship('OrdemServico', back_populates='itens')
    item = db.relationship('Estoque')
