from flask import Flask, jsonify, request, abort
import json
import jwt
import time
from Modelos.Usuarios import User
from Modelos.Hilos import Hilo
from Modelos.Comentarios import Comentario
from pymongo import MongoClient
from datetime import datetime, timedelta
from functools import wraps
application = Flask(__name__)

TOKEN_KEY = "top secret"

client = MongoClient(
    'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
db = client.proyecto

users = []
hilos = []

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kargs):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            try:
                data = jwt.decode(token, TOKEN_KEY, algorithms=["HS256"])
                user = data['user']
                return f(user, *args, **kargs)
            except:
                abort(401)
        abort(401)
    return decorated


@application.route('/')
def root():
    return 'API Levantada'


@application.route('/login', methods=['POST'])
def login():
    isUser = 'usuario' in request.json
    isPass = 'password' in request.json
    if isUser and isPass:
        user = request.json['usuario']
        password = request.json['password']
        if password == getUserPassword(users,user):
            token = jwt.encode(
                {
                    "user": getUserName(users,user),
                    "exp": datetime.utcnow() + timedelta(seconds=24 * 3500)
                },
                TOKEN_KEY,
                algorithm="HS256")
            return jsonify({'RESULTADO': token}), 200
        return jsonify({'RESULTADO': 'Login incorrecto'}), 400
    return jsonify({'RESULTADO': 'Faltan datos'}), 400


@application.route('/logon', methods=['POST'])
def logon():
    isUser = 'usuario' in request.json
    isPass = 'password' in request.json
    isName = 'name' in request.json
    if isUser and isPass and isName:
        db.usuarios.insert_one({
            "user": request.json['usuario'],
            "password": request.json['password'],
            "name": request.json['name']
        })
        getAllUsers(db)
        return jsonify({'RESULTADO': 'Registro completo'}), 200
    return jsonify({'RESULTADO': 'Faltan datos'}), 400


@application.route('/datos', methods=['GET'])
@auth_required
def datos(user):
    return jsonify({'datos': user}), 200


@application.route('/datos/<nombre>', methods=['GET'])
@auth_required
def datos_name(user, nombre):
    return jsonify({'datos': nombre}), 200

@application.route('/hilos', methods=['GET'])
def datos_hilos():
    titulos = ""
    for hilo in hilos:
        titulos += hilo.getTitulo() + ","
    return jsonify({'RESULTADO': titulos[0:len(titulos)-1]}), 200

@application.route('/hilos', methods=['POST'])
@auth_required
def setHilo(user):
    isTitulo = 'titulo_hilo' in request.json
    isAutor = 'autor_hilo' in request.json
    if isTitulo and isAutor:
        db.hilos.insert_one({
            "titulo_hilo": request.json['titulo_hilo'],
            "autor_hilo": request.json['autor_hilo'],
            "comentarios": request.json['comentarios']
        })
        getAllHilos(db)
        return jsonify({'RESULTADO': 'Registro completo'}), 200
    return jsonify({'RESULTADO': 'Faltan datos'}), 400

@application.errorhandler(401)
def unauthorized(e):
    return jsonify({'Error': 'No estás autenticado'}), 401

def getAllHilos(db):
    _hilos=[]
    hilos.clear()
    _hilos = db.hilos.find()
    for _hilo in _hilos:
        hilos.append(Hilo(_hilo))

def getAllUsers(db):
    _users = []
    users.clear()
    _users = db.usuarios.find()
    for _user in _users:
        users.append(User(_user))

        
def getUserPassword(users, username):
    for user in users:
        if user.getUser() == username:
            return user.getPassword()
    return "vacio"

def getUserName(users,username):
    for user in users:
        if user.getUser() == username:
            return user.getName()
    return "Anonimo"


if __name__ == '__main__':
    getAllUsers(db)
    getAllHilos(db)
    application.run(debug=True)


