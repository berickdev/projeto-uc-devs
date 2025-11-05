from flask import Blueprint, request, jsonify
from app import db
from app.models import Cliente

# Define o Blueprint
bp_clientes = Blueprint('clientes', __name__)

# --- ROTAS CRUD PARA CLIENTES ---

@bp_clientes.route('', methods=['POST'])
def create_cliente():
    """Cria um novo cliente."""
    try:
        data = request.get_json()
        
        # Validação simples de dados
        if not data or 'nome' not in data or 'email' not in data:
            return jsonify({'erro': 'Dados incompletos (nome e email obrigatórios)'}), 400
        
        # Verifica se o email já existe
        if Cliente.query.filter_by(email=data['email']).first():
            return jsonify({'erro': 'Email já cadastrado'}), 409 # 409 Conflict
            
        novo_cliente = Cliente(
            nome=data['nome'],
            email=data['email'],
            telefone=data.get('telefone') # .get() é seguro se a chave não existir
        )
        
        db.session.add(novo_cliente)
        db.session.commit()
        
        # Retorna o cliente criado com o ID
        return jsonify({
            'id': novo_cliente.id,
            'nome': novo_cliente.nome,
            'email': novo_cliente.email,
            'telefone': novo_cliente.telefone
        }), 201 # 201 Created
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro interno ao criar cliente: {str(e)}'}), 500

@bp_clientes.route('', methods=['GET'])
def get_all_clientes():
    """Retorna todos os clientes."""
    try:
        clientes = Cliente.query.all()
        
        # Converte a lista de objetos Cliente para uma lista de dicionários
        output = [
            {'id': c.id, 'nome': c.nome, 'email': c.email, 'telefone': c.telefone} 
            for c in clientes
        ]
        
        return jsonify(output), 200
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@bp_clientes.route('/<int:id>', methods=['GET'])
def get_cliente_by_id(id):
    """Retorna um cliente específico pelo ID."""
    try:
        cliente = Cliente.query.get(id)
        
        if not cliente:
            return jsonify({'erro': 'Cliente não encontrado'}), 404
            
        return jsonify({
            'id': cliente.id,
            'nome': cliente.nome,
            'email': cliente.email,
            'telefone': cliente.telefone
        }), 200
        
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@bp_clientes.route('/<int:id>', methods=['PUT'])
def update_cliente(id):
    """Atualiza um cliente existente."""
    try:
        cliente = Cliente.query.get(id)
        
        if not cliente:
            return jsonify({'erro': 'Cliente não encontrado'}), 404
            
        data = request.get_json()
        
        # Validação de email duplicado (se o email foi alterado)
        novo_email = data.get('email')
        if novo_email and novo_email != cliente.email:
            if Cliente.query.filter_by(email=novo_email).first():
                return jsonify({'erro': 'Email já cadastrado por outro usuário'}), 409
        
        # Atualiza os campos
        cliente.nome = data.get('nome', cliente.nome)
        cliente.email = data.get('email', cliente.email)
        cliente.telefone = data.get('telefone', cliente.telefone)
        
        db.session.commit()
        
        return jsonify({'id': cliente.id, 'nome': cliente.nome}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@bp_clientes.route('/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    """Exclui um cliente."""
    try:
        cliente = Cliente.query.get(id)
        
        if not cliente:
            return jsonify({'erro': 'Cliente não encontrado'}), 404
        
        # (Futuramente, teremos que verificar se o cliente tem atendimentos
        # antes de excluir, mas por enquanto vamos fazer a exclusão direta)
            
        db.session.delete(cliente)
        db.session.commit()
        
        return jsonify({'mensagem': 'Cliente excluído com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        # Tratamento especial para erro de chave estrangeira (se ele tiver atendimentos)
        if 'foreign key constraint' in str(e).lower():
            return jsonify({'erro': 'Não é possível excluir: Cliente possui atendimentos registrados.'}), 400
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500