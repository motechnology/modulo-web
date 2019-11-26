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
listaIDs = dados.distinct("id")


app = Flask(__name__)


@app.route('/medicoes', methods=['GET'])
def get_medicoes():
   # print("Sem dumps: ", dados.find(manipulate=False))
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
            data_str, "%d/%m/%Y %H:%M").timestamp()
        dicionario['data'] = data

    dados.insert(dicionario, manipulate=False)
    print(dicionario)

    return dicionario, 201


@app.route('/medicoes.html', methods=['GET'])
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
    pagina += "        }\n"    else:
62
        dicionario['temperatura'] = t
63
​
64
    try:
65
        data_str = request.json.get('data')
66
    except:
67
        pass
68
    else:
69
        data = datetime.datetime.strptime(
70
            data_str, "%d/%m/%Y %H:%M").timestamp()
71
        dicionario['data'] = data
72
​
73
    dados.insert(dicionario, manipulate=False)
74
    print(dicionario)
75
​
76
    return dicionario, 201
77
​
78
​
79
@app.route('/medicoes.html', methods=['GET'])
80
def geraGraficos():
81
​
82
    pagina = """
83
    <!DOCTYPE html>
84
    <html>
85
    <head>
86
            <meta charset = "utf-8" >
87
            <title> Lendo a temperatura com o Arduino </title >
88
            <link href="https://cdn.jsdelivr.net/chartist.js/latest/chartist.min.css" rel="stylesheet" type="text/css" />
89
        </head>
90
​
91
        <body>
92
            <div class="ct-chart ct-major-seventh"></div>
93
            <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.js"></script>
94
​
95
            <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/locale/pt-br.js"></script>
96
            <script src="https://cdn.jsdelivr.net/chartist.js/latest/chartist.min.js"></script>
97
            <script>
98
    """
99
    pagina += "new Chartist.Line('.ct-chart', {\n"
100
    pagina += "series: [ \n"
101
    for idArd in listaIDs:
102
        pagina += "{\n"
103
        pagina += "name: '" + idArd + "',\n"
104
        pagina += "data: [\n"
105
        for dadosLidos in dados.find({'id': idArd}):
106
            pagina += "{x: new Date(" + str(dadosLidos['data'] * 1000) + ")" + ", y:" + str(
107
                dadosLidos['umidade']) + "},\n"
108
        pagina += "     ]\n"  # colchete do data
109
        pagina += "},\n"  # chave do {\n
110
    pagina += "] \n"  # colchete da série
111
    pagina += "},\n"  # chave da função new Chartist....
112
    pagina += "{\n"
113
    pagina += "    axisX: {\n"
114
    pagina += "        type: Chartist.FixedScaleAxis,\n"
115
    pagina += "        divisor: 5,\n"
116
    pagina += "        labelInterpolationFnc: function (value) {\n"
117
    pagina += "            return moment(value).format('HH:MM-DD/MM');\n"
118
    pagina += "        }\n"
119
    pagina += "    }\n"
120
    pagina += "});\n"
121
    pagina += " </script>\n"
122
    pagina += "  </body>\n"
123
    pagina += "</html>\n"
124
​
125
    return pagina, 200
126
​
127
​
128
@app.route('/medicoes/<ard_id>')
129
def geraGraficoUmArduino():
130
    pass
131
​
132
​
133
if __name__ == "__main__":
134
    app.run(debug=True, host='127.0.0.1', port=5000)
    pagina += "    }\n"
    pagina += "});\n"
    pagina += " </script>\n"
    pagina += "  </body>\n"
    pagina += "</html>\n"

    pagina += """
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


@app.route('/medicoes/<ard_id>')
def geraGraficoUmArduino():
    pass


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
