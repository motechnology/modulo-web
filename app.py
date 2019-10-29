from flask import Flask, jsonify
from flask import abort
from flask import request
from flask import json
import pprint
import pymongo
import time
import datetime
from pymongo import MongoClient
from bson.json_util import dumps

cliente = MongoClient('127.0.0.1')
db = cliente.test
dados = db.medicoes
users = db.arduino

app = Flask(__name__)


@app.route('/medicoes', methods=['GET'])
def get_medicoes():
    print("Sem dumps: ", dados.find(manipulate=False))
    return dumps(dados.find({}, {'_id': False, 'id': True, 'umidade': True, 'temperatura': True, 'data': True})), 200

# Retorna os dados de mediçao de um unico arduino
@app.route('/medicoes/<ard_id>', methods=['GET'])
def get_med(ard_id):
    return dumps(dados.find_one({},{'_id': False, 'id': ard_id, 'umidade': True, 'temperatura': True, 'data': True})), 200

# Método post para adicionar novas medicoes
@app.route('/medicoes', methods=['POST'])
def post_medida():
    dicionario = dict()

    if not request.json or not 'id' in request.json:
        abort(400)

    # Verifica nome do usuário
    try:
        dicionario['id'] = request.json['id']
        dicionario['s'] = request.json['s']
    except:
        return "Bad Request", 400
    else:
        usuario = users.find_one(dicionario)
        if usuario is None:
            return "Unauthorized", 401

    try:
        u = int(request.json.get('u'))
    except:
        pass
    else:
        dicionario['umidade'] = u

    try:
        t = int(request.json.get('t'))
    except:
        pass
    else:
        dicionario['temperatura'] = t
    try:
        data_str = request.json.get('data')
    except:
        pass
    else:
        data = datetime.datetime.strptime(
            data_str, "%d/%m/%Y %H:%M:%S").timestamp()
        dicionario['data'] = data

    dados.insert(dicionario, manipulate=False)
    print(dicionario)

    return dicionario, 201


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
