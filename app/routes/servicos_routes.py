from flask import Blueprint, request, jsonify
from app import db
from app.models import Servico

# Define o Blueprint
bp_servicos = Blueprint('servicos', __name__)

# --- ROTAS CRUD PARA SERVIÇOS ---

@bp_servicos.route('', methods=['POST'])
def create_servico():
    """Cria um novo serviço."""
    try:
        data = request.get_json()
        
        if not data or 'descricao' not in data or 'valor' not in data:
            return jsonify({'erro': 'Dados incompletos (descrição e valor obrigatórios)'}), 400
        
        novo_servico = Servico(
            descricao=data['descricao'],
            valor=float(data['valor'])
        )
        
        db.session.add(novo_servico)
        db.session.commit()
        
        return jsonify({
            'id': novo_servico.id,
            'descricao': novo_servico.descricao,
            'valor': novo_servico.valor
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@bp_servicos.route('', methods=['GET'])
def get_all_servicos():
    """Retorna todos os serviços."""
    try:
        servicos = Servico.query.all()
        output = [
            {'id': s.id, 'descricao': s.descricao, 'valor': s.valor} 
            for s in servicos
        ]
        return jsonify(output), 200
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@bp_servicos.route('/<int:id>', methods=['PUT'])
def update_servico(id):
    """Atualiza um serviço."""
    try:
        servico = Servico.query.get(id)
        if not servico:
            return jsonify({'erro': 'Serviço não encontrado'}), 404
            
        data = request.get_json()
        
        servico.descricao = data.get('descricao', servico.descricao)
        servico.valor = float(data.get('valor', servico.valor))
        
        db.session.commit()
        
        return jsonify({'id': servico.id, 'descricao': servico.descricao}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@bp_servicos.route('/<int:id>', methods=['DELETE'])
def delete_servico(id):
    """Exclui um serviço."""
    try:
        servico = Servico.query.get(id)
        if not servico:
            return jsonify({'erro': 'Serviço não encontrado'}), 404
            
        db.session.delete(servico)
        db.session.commit()
        
        return jsonify({'mensagem': 'Serviço excluído com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        if 'foreign key constraint' in str(e).lower():
            return jsonify({'erro': 'Não é possível excluir: Serviço está vinculado a atendimentos.'}), 400
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500