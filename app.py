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
   #print("Sem dumps: ", dados.find(manipulate=False))
    return dumps(dados.find({}, {'_id': False, 'id': True, 'umidade': True, 'temperatura': True, 'data': True})), 200

# Retorna os dados de mediçao de um unico arduino
@app.route('/medicoes/<ard_id>', methods=['GET'])
def get_med(ard_id):
    return dumps(dados.find({'id': ard_id}, {'_id': False, 'id': ard_id, 'umidade': True, 'temperatura': True, 'data': True})), 200

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
            data_str, "%d/%m/%Y %H:%M").timestamp()
        dicionario['data'] = data

    dados.insert(dicionario, manipulate=False)
    print(dicionario)

    return dicionario, 201


@app.route('/medicoes')
def geraGraficos():
    pagina = """
<!DOCTYPE html>
<html>
   <head>
        <meta charset = "utf-8" >
        <title> Lendo a temperatura com o Arduino </title >
        <link href="https://cdn.jsdelivr.net/chartist.js/latest/chartist.min.css" rel="stylesheet" type="text/css" />
    </head>

    <body>
        <div class="ct-chart ct-major-seventh"></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.js"></script>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/locale/pt-br.js"></script>
        <script src="https://cdn.jsdelivr.net/chartist.js/latest/chartist.min.js"></script>
        <script>
"""
    pagina += "new Chartist.Line('.ct-chart', {\n"
    pagina += "series: [ \n"

    for dadosLidos in dados:
        pagina += "{\n"
        pagina += "            name: '" + "Arduinos do sistema de medição" + "',\n"
        pagina += "            data: [\n"
        pagina += "{x: new Date(" + dadosLidos['data'] * 1000 + ")" + \
            " " + dadosLidos['id'] + "y:" + dadosLidos['u'] + "},\n"
        pagina += "]"
        pagina += "},"

    pagina += "series: [ \n"
    for dadosLidos in dados:
        pagina += "{\n"
        pagina += "            name: '" + "Arduinos do sistema de medição" + "',\n"
        pagina += "            data: [\n"
        pagina += "{x: new Date(" + dadosLidos['data'] * 1000 + ")" + \
            " " + dadosLidos['id'] + ", y:" + dadosLidos['t'] + "},\n"
        pagina += "]"
        pagina += "},"

    pagina += "{\n"
    pagina += "    axisX: {\n"
    pagina += "        type: Chartist.FixedScaleAxis,\n"
    pagina += "        divisor: 5,\n"
    pagina += "        labelInterpolationFnc: function (value) {\n"
    pagina += "            return moment(value).format('HH:MM-DD/MM');\n"
    pagina += "        }\n"
    pagina += "    }\n"
    pagina += "});\n"
    pagina += " </script>\n"
    pagina += "  </body>\n"
    pagina += "</html>\n"

    return pagina, 200


@app.route('/medicoes/<ard_id>')
def geraGraficoUmArduino():
    pass


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
