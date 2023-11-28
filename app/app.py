from flask import Flask, jsonify, render_template
from logging import FileHandler, WARNING
import sys
import os
import mysql.connector

app = Flask(__name__, template_folder = 'templates')

def datos_participantes():

    config = {
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': 'db',
        'port': '3306',
        'database': 'dbproyecto'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT NOMBRE_ALUMNO, CARRERA FROM participantes')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results


@app.route('/index')
@app.route('/')
def index():
    participantes = datos_participantes()
    return render_template('index.html', participantes=participantes)

@app.route('/participantes')
def estudiantes():
    return jsonify({'estudiantes': datos_participantes()})

@app.route('/probando')
def hola():
    return 'hola!!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
