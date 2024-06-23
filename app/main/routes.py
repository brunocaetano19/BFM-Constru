from flask import render_template, request, redirect, url_for
from app import db
from app.models import Estoque, OrdemServico, ItemOrdemServico
from . import bp

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/estoque')
def estoque():
    itens = Estoque.query.all()
    return render_template('estoque.html', itens=itens)

@bp.route('/adicionar_item', methods=['POST'])
def adicionar_item():
    nome = request.form['nome']
    quantidade = int(request.form['quantidade'])
    item = Estoque(nome=nome, quantidade_disponivel=quantidade, quantidade_reservada=0)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('main.estoque'))

@bp.route('/ordens_servico')
def ordens_servico():
    ordens = OrdemServico.query.all()
    return render_template('ordens_servico.html', ordens=ordens)

@bp.route('/nova_ordem', methods=['GET', 'POST'])
def nova_ordem():
    if request.method == 'POST':
        cliente = request.form['cliente']
        ordem = OrdemServico(cliente=cliente)
        db.session.add(ordem)
        db.session.commit()
        return redirect(url_for('main.ordens_servico'))
    return render_template('ordem_servico.html')

@bp.route('/ordem/<int:ordem_id>', methods=['GET', 'POST'])
def ordem(ordem_id):
    ordem = OrdemServico.query.get(ordem_id)
    itens = Estoque.query.all()
    if request.method == 'POST':
        item_id = int(request.form['item_id'])
        quantidade = int(request.form['quantidade'])
        item_ordem = ItemOrdemServico(ordem_id=ordem_id, item_id=item_id, quantidade=quantidade)
        db.session.add(item_ordem)

        item = Estoque.query.get(item_id)
        item.quantidade_disponivel -= quantidade
        item.quantidade_reservada += quantidade

        db.session.commit()
        return redirect(url_for('main.ordens_servico'))

    return render_template('ordem_servico.html', ordem=ordem, itens=itens)

@bp.route('/finalizar_ordem/<int:ordem_id>', methods=['POST'])
def finalizar_ordem(ordem_id):
    ordem = OrdemServico.query.get(ordem_id)
    ordem.status = 'finalizado'

    for item in ordem.itens:
        item_no_estoque = Estoque.query.get(item.item_id)
        item_no_estoque.quantidade_reservada -= item.quantidade

    db.session.commit()
    return redirect(url_for('main.ordens_servico'))
