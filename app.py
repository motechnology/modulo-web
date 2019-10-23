from flask import Flask, jsonify
from flask import abort
from flask import request
from flask import json

import pprint
import pymongo
from bson.raw_bson import RawBSONDocument
from pymongo import MongoClient
from bson.json_util import dumps

cliente = MongoClient('127.0.0.1')
db = cliente.test
dados = db.medicoes
users = db.arduinos


app = Flask(__name__)

@app.route('/medicoes', methods=['GET'])
def get_medicoes():
    print(dumps(dados.find()))
    return jsonify(dumps(dados.find())), 200

# Retorna os dados de mediçao de um unico arduino
@app.route('/medicoes/<int:ard_id>', methods=['GET'])
def get_med(ard_id):
    return jsonify(dumps(dados.find_one({'id': ard_id}))), 200

# Método post para adicionar novas medicoes
@app.route('/medicoes', methods=['POST'])
def post_medida():
    if not request.json or not 'id' in request.json:
        abort(400)
    try:
        nova_medicao = {
            'id': request.json['id'],
            'u': request.json.get('u', ""),
            't': request.json.get('t', ""),
            'tm': request.json.get('tm')
        }
        dados.insert_one(nova_medicao)
        return jsonify(dumps(nova_medicao)), 201
    except Exception as e:
        abort(401)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
