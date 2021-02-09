from flask import Flask, jsonify, request, abort
import json
import jwt
import time
from Modelos.Usuarios import User
from pymongo import MongoClient
from datetime import datetime, timedelta
from functools import wraps
application = Flask(__name__)

TOKEN_KEY = "top secret"

client = MongoClient(
    'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
db = client.proyecto

users = []

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
    return jsonify({'Hola': nombre}), 200


@application.errorhandler(401)
def unauthorized(e):
    return jsonify({'Error': 'No estás autenticado'}), 401


def getAllUsers(db):
    _users = []
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
    application.run(debug=True)


