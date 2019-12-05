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
import os

cliente = MongoClient('127.0.0.1')
db = cliente.test
dados = db.medicoes
users = db.arduino
listaIDs = dados.distinct("id")

app = Flask(__name__)


# Método post para adicionar novas medicoes
@app.route('/medicoes', methods=['POST'])
def post_medida():
    novaMedida = dict()

    if not request.json or not 'id' in request.json:
        abort(400)
    #Verifica se o arduino que encaminhou a medição está contido na coleção de arduinos do
    #sistema de coleta
    try:
        novaMedida['id'] = request.json['id']
        novaMedida['s'] = request.json['s']
    except:
        return "Bad Request", 400
    else:
        usuario = users.find_one(novaMedida)
        if usuario is None:
            return "Unauthorized", 401

    try:
        u = int(request.json.get('u'))
    except:
        pass
    else:
        novaMedida['umidade'] = u

    try:
        t = int(request.json.get('t'))
    except:
        pass
    else:
        novaMedida['temperatura'] = t

    try:
        data_str = request.json.get('data')
    except:
        pass
    else:
        data = datetime.datetime.strptime(
            data_str, "%d/%m/%Y %H:%M").timestamp()
        novaMedida['data'] = data

    dados.insert(novaMedida, manipulate=False)
    print(novaMedida)

    return novaMedida, 201


#Método para retornar gráficos com todos os arduinos do sistema
@app.route('/medicoes', methods=['GET'])
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
            <div style="display:flex; flex-direction: row; justify-content: center; align-items: center">
                <h1>Umidade (%)</h1>
                <div class="ct-chart ct-major-seventh" id="chart1"></div>
            </div>
            <center><h1>Data da coleta</h1></center>
            <div style="display:flex; flex-direction: row; justify-content: center; align-items: center">
                <h1>Temperatura (°C)</h1>
                <div class="ct-chart ct-major-seventh" id="chart2"></div>
            </div>
            <center><h1>Data da coleta</h1></center>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/locale/pt-br.js"></script>
            <script src="https://cdn.jsdelivr.net/chartist.js/latest/chartist.min.js"></script>
            <script>
    """
    pagina += "new Chartist.Line('#chart1', {\n"
    pagina += "series: [ \n"
    for idArd in listaIDs:
        pagina += "{\n"
        pagina += "name: '" + idArd + "',\n"
        pagina += "data: [\n"
        for dadosLidos in dados.find({'id': idArd}):
            pagina += "{x: new Date(" + str(dadosLidos['data'] * 1000) + ")" + ", y:" + str(
                dadosLidos['umidade']) + "},\n"
        pagina += "     ]\n"  # colchete do data
        pagina += "},\n"  # chave do {\n
    pagina += "] \n"  # colchete da série
    pagina += "},\n"  # chave da função new Chartist....
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

    pagina += """
    <script>
    """
    pagina += "new Chartist.Line('#chart2', {\n"
    pagina += "series: [ \n"
    for idArd in listaIDs:
        pagina += "{\n"
        pagina += "name: '" + idArd + "',\n"
        pagina += "data: [\n"
        for dadosLidos in dados.find({'id': idArd}):
            pagina += "{x: new Date(" + str(dadosLidos['data'] * 1000) + ")" + ", y:" + str(
                dadosLidos['temperatura']) + "},\n"
        pagina += "     ]\n"  # colchete do data
        pagina += "},\n"  # chave do {\n
    pagina += "] \n"  # colchete da série
    pagina += "},\n"  # chave da função new Chartist....
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

#Método para retornar gráfico de um arduino específico
@app.route('/medicoes/<ard_id>', methods=['GET'])
def geraGraficoUmArduino(ard_id):
    pagina = pagina = """
    <!DOCTYPE html>
    <html>
    <head>
            <meta charset = "utf-8" >
            <title> Lendo a temperatura com o Arduino </title >
            <link href="https://cdn.jsdelivr.net/chartist.js/latest/chartist.min.css" rel="stylesheet" type="text/css" />
        </head>
        <body>
            <div style="display:flex; flex-direction: row; justify-content: center; align-items: center">
                <h1>Umidade (%)</h1>
                <div class="ct-chart ct-major-seventh" id="chart1"></div>
            </div>
            <center><h1>Data da coleta</h1></center>
            <div style="display:flex; flex-direction: row; justify-content: center; align-items: center">
                <h1>Temperatura (°C)</h1>
                <div class="ct-chart ct-major-seventh" id="chart2"></div>
            </div>
            <center><h1>Data da coleta</h1></center>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/locale/pt-br.js"></script>
            <script src="https://cdn.jsdelivr.net/chartist.js/latest/chartist.min.js"></script>
            <script>
    """
    pagina += "new Chartist.Line('#chart1', {\n"
    pagina += "series: [ \n"
    pagina += "{\n"
    pagina += "name: '" + ard_id + "',\n"
    pagina += "data: [\n"
    for dadosLidos in dados.find({'id': ard_id}):
        pagina += "{x: new Date(" + str(dadosLidos['data'] * 1000) + ")" + ", y:" + str(
            dadosLidos['umidade']) + "},\n"
    pagina += "     ]\n"  # colchete do data
    pagina += "},\n"  # chave do {\n
    pagina += "] \n"  # colchete da série
    pagina += "},\n"  # chave da função new Chartist....
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

    pagina += """
    <script>
    """
    pagina += "new Chartist.Line('#chart2', {\n"
    pagina += "series: [ \n"
    pagina += "{\n"
    pagina += "name: '" + ard_id + "',\n"
    pagina += "data: [\n"
    for dadosLidos in dados.find({'id': ard_id}):
        pagina += "{x: new Date(" + str(dadosLidos['data'] * 1000) + ")" + ", y:" + str(
            dadosLidos['temperatura']) + "},\n"
    pagina += "     ]\n"  # colchete do data
    pagina += "},\n"  # chave do {\n
    pagina += "] \n"  # colchete da série
    pagina += "},\n"  # chave da função new Chartist....
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


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
