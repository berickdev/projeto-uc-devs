from flask import Blueprint, request, jsonify
from app import db
from app.models import Atendimento, Cliente, Servico

bp_atendimentos = Blueprint('atendimentos', __name__)

@bp_atendimentos.route('', methods=['POST'])
def create_atendimento():
    try:
        data = request.get_json()

        cliente_id = data.get('cliente_id')
        servico_id = data.get('servico_id')

        if not cliente_id or not servico_id:
            return jsonify({'erro': 'IDs do cliente e do serviço são obrigatórios'}), 400
        
        if not Cliente.query.get(cliente_id):
            return jsonify({'erro':'Cliente não encontrado'}), 404
        if not Servico.query.get(servico_id):
            return jsonify({'erro':'servico não encontrado'}), 404
        
        novo_atendimento = Atendimento(
            cliente_id=cliente_id,
            servico_id=servico_id,
            observacoes=data.get('observacoes')
        )

        db.session.add(novo_atendimento)
        db.session.commit()

        return jsonify({'mensagem':'Atendimento registrado com sucesso', 'id': novo_atendimento.id}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500
    
@bp_atendimentos.route('', methods=['GET'])
def get_all_atendimentos():
    try:
        atendimentos = Atendimento.query.all()
        output = []

        for atendimento in atendimentos:
            output.append({
                'id':atendimento.id,
                'data':atendimento.data.isoformat(),
                'observacoes':atendimento.observacoes,
                'cliente_id':atendimento.cliente_id,
                'cliente_nome':atendimento.cliente.nome,
                'servico_id':atendimento.servico_id,
                'servico_descricao':atendimento.servico.descricao,
                'servico_valor':atendimento.servico.valor
            })

        return jsonify(output), 200
    
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500
    
@bp_atendimentos.route('', methods=['DELETE'])
def delete_atendimentos(id):
    try:
        atendimento = Atendimento.query.get(id)

        if not atendimento:
            return jsonify({'erro': 'Atendimento não encontrado'}), 404
        
        db.session.delete(atendimento)
        db.session.commit()

        return jsonify({'mensagem': 'Atendimento excluido com sucesso'}),200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro interno: {str(e)}'}),500