from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Configuração do banco PostgreSQL (Render)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Chave JWT (variável de ambiente no Render)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# Inicializações
db = SQLAlchemy(app)
jwt = JWTManager(app)

# MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")

    def __init__(self, usuario, senha, role="user"):
        self.usuario = usuario
        self.senha = generate_password_hash(senha)
        self.role = role

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

# ROTAS
@app.route("/")
def home():
    return "API rodando com Flask + SQLAlchemy + JWT!"

# Criar conta
@app.route("/register", methods=["POST"])
def register():
    dados = request.json
    usuario = dados.get("usuario")
    senha = dados.get("senha")
    role = dados.get("role", "user")

    if User.query.filter_by(usuario=usuario).first():
        return jsonify(msg="Usuário já existe"), 400

    novo_user = User(usuario=usuario, senha=senha, role=role)
    db.session.add(novo_user)
    db.session.commit()
    return jsonify(msg=f"Usuário {usuario} criado com sucesso!"), 201

# Login
@app.route("/login", methods=["POST"])
def login():
    dados = request.json
    usuario = dados.get("usuario")
    senha = dados.get("senha")

    user = User.query.filter_by(usuario=usuario).first()
    if user and check_password_hash(user.senha, senha):
        token = create_access_token(identity=user.usuario)
        return jsonify(access_token=token), 200
    else:
        return jsonify(msg="Usuário ou senha inválidos"), 401

# CRUD de Clientes
@app.route("/clientes", methods=["POST"])
@jwt_required()
def criar_cliente():
    usuario_logado = get_jwt_identity()
    user = User.query.filter_by(usuario=usuario_logado).first()

    if user.role != "admin":
        return jsonify(msg="Acesso negado. Apenas admin pode criar clientes."), 403

    dados = request.json
    nome = dados.get("nome")

    novo_cliente = Cliente(nome=nome)
    db.session.add(novo_cliente)
    db.session.commit()
    return jsonify(msg="Cliente criado com sucesso!"), 201

@app.route("/clientes", methods=["GET"])
@jwt_required()
def listar_clientes():
    clientes = Cliente.query.all()
    lista = [{"id": c.id, "nome": c.nome} for c in clientes]
    return jsonify(lista), 200

@app.route("/clientes/<int:id>", methods=["PUT"])
@jwt_required()
def editar_cliente(id):
    usuario_logado = get_jwt_identity()
    user = User.query.filter_by(usuario=usuario_logado).first()

    if user.role != "admin":
        return jsonify(msg="Acesso negado. Apenas admin pode editar clientes."), 403

    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify(msg="Cliente não encontrado"), 404

    dados = request.json
    cliente.nome = dados.get("nome", cliente.nome)
    db.session.commit()
    return jsonify(msg="Cliente atualizado com sucesso!"), 200

@app.route("/clientes/<int:id>", methods=["DELETE"])
@jwt_required()
def excluir_cliente(id):
    usuario_logado = get_jwt_identity()
    user = User.query.filter_by(usuario=usuario_logado).first()

    if user.role != "admin":
        return jsonify(msg="Acesso negado. Apenas admin pode excluir clientes."), 403

    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify(msg="Cliente não encontrado"), 404

    db.session.delete(cliente)
    db.session.commit()
    return jsonify(msg="Cliente excluído com sucesso!"), 200

# Inicialização
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # cria tabelas no banco do Render
    app.run(debug=True)
