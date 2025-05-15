from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qgaJdQPJNyCSQNCfKaxuxlfqptrnrmjI@mainline.proxy.rlwy.net:52866/railway'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/adicionar', methods=['POST'])
def adicionar_produto():
    data = request.json
    novo_produto = Produto(nome=data['nome'])
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify({'mensagem': 'Produto adicionado!'})

@app.route('/listar', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([{'id': p.id, 'nome': p.nome} for p in produtos])

@app.route('/excluir/<int:id>', methods=['DELETE'])
def excluir_produto(id):
    produto = Produto.query.get(id)
    if produto:
        db.session.delete(produto)
        db.session.commit()
        return jsonify({'mensagem': 'Produto excluído!'})
    return jsonify({'mensagem': 'Produto não encontrado!'}), 404

@app.route('/editar/<int:id>', methods=['PUT'])
def editar_produto(id):
    data = request.json
    produto = Produto.query.get(id)
    if produto:
        produto.nome = data['nome']
        db.session.commit()
        return jsonify({'mensagem': 'Produto atualizado!'})
    return jsonify({'mensagem': 'Produto não encontrado!'}), 404

import os

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
