from flask import Blueprint, render_template

bp_views = Blueprint('views', __name__)

@bp_views.route('/')
def index():
    return render_template('dashboard.html')

@bp_views.route('/clientes')
def clientes_page():
    return render_template('clientes.html')

@bp_views.route('/atendimentos')
def atendimentos_page():
    return render_template('atendimentos.html')

@bp_views.route('/servicos')
def servicos_page():
    return render_template('servicos.html')