from flask import Flask, jsonify, request, abort
import os
import jwt
import hashlib
from Modelos.Usuarios import User
from Modelos.Hilos import Hilo
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from functools import wraps
application = Flask(__name__)

TOKEN_KEY = "copa"

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
                id = data['_id']
                return f(user,id, *args, **kargs)
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
        usuario = []
        usuario = db.usuarios.find_one({
            "user":user
        })
        if usuario is not None:
            password_hash = hashlib.sha512(password.encode('utf-8') + usuario['salt']).hexdigest()
            print(password_hash)
            if usuario['password'] == password_hash:
                token = jwt.encode(
                    {
                        "_id": str(ObjectId(usuario['_id'])),
                        "user": getUserName(users, user),
                        "exp": datetime.utcnow() + timedelta(seconds=24 * 3500)
                    },
                    TOKEN_KEY,
                    algorithm="HS256")
                return jsonify({'RESULTADO': token}), 200
        return jsonify({'RESULTADO': 'Login incorrecto'}), 403
    return jsonify({'RESULTADO': 'Faltan datos'}), 400


@application.route('/logon', methods=['POST'])
def logon():
    isUser = 'usuario' in request.json
    isPass = 'password' in request.json
    isName = 'name' in request.json
    if isUser and isPass and isName:
        password = request.json['password']
        salt = os.urandom(16)
        password_hash = hashlib.sha512(password.encode('utf-8') + salt).hexdigest()
        db.usuarios.insert_one({
            "user": request.json['usuario'],
            "password": password_hash,
            "name": request.json['name'],
            "salt" : salt
        })
        getAllUsers(db)
        return jsonify({'RESULTADO': 'Registro completo'}), 200
    return jsonify({'RESULTADO': 'Faltan datos'}), 400


@application.route('/datos', methods=['GET'])
@auth_required
def datos(user,id):
    return jsonify({'datos': user}), 200


@application.route('/datosId', methods=['GET'])
@auth_required
def datos_name(user, id):
    return jsonify({'datos': id}), 200


@application.route('/hilos', methods=['GET'])
def datos_hilos():
    titulos = ""
    autores =""
    for hilo in hilos:
        titulos += hilo.getTitulo() + ","
        autores += hilo.getAutor() + ","
    return jsonify({'Hilos': titulos[0:len(titulos)-1],'Autores':autores[0:len(autores)-1]}), 200


@application.route('/hilo', methods=['POST'])
@auth_required
def setHilo(user, id):
    isTitulo = 'titulo_hilo' in request.json
    isAutor = 'autor_hilo' in request.json
    if isTitulo and isAutor:
        db.hilos.insert_one({
            "titulo_hilo": request.json['titulo_hilo'],
            "autor_hilo": request.json['autor_hilo']
        })
        getAllHilos(db)
        return jsonify({'RESULTADO': 'Registro completo'}), 200
    return jsonify({'RESULTADO': 'Faltan datos'}), 400


@application.route('/hilo', methods=['DELETE'])
@auth_required
def deleteHilo(user, id):
    isTitulo = 'titulo_hilo' in request.json
    if isTitulo:
        db.hilos.delete_one({
            "titulo_hilo": request.json['titulo_hilo']
        })
        getAllHilos(db)
        return jsonify({'RESULTADO': 'Registro completo'}), 200
    return jsonify({'RESULTADO': 'Faltan datos'}), 400


@application.route('/hilo/comentarios', methods=['GET'])
def getComentarioHilo():

    _comentarios = ""
    isHilo = 'titulo_hilo' in request.json
    if isHilo:
        for hilo in hilos:
            if hilo.getTitulo() == request.json["titulo_hilo"] and hilo.haveComentarios():
                for _comentario in hilo.getComentarios():
                    _comentarios += _comentario[0]+","+_comentario[1]+";"
                return jsonify({'RESULTADO':  _comentarios[0:len(_comentarios)-1]}), 200
            return jsonify({'RESULTADO': 'No contiene comentarios'}), 201
    else:
        return jsonify({'RESULTADO': 'Faltan datos'}), 400


@application.route('/hilo/comentarios', methods=['PUT'])
@auth_required
def setComentarioHilo(user, id):
    isComentario = "texto_comentario" in request.json
    isAutorC = "autor_comentario" in request.json
    isHilo = "titulo_hilo" in request.json
    isAutorH = "autor_hilo" in request.json
    if isComentario and isAutorC and isHilo and isAutorH:
        db.hilos.update_one({"titulo_hilo":request.json["titulo_hilo"],"autor_hilo":request.json["autor_hilo"]}, {
                    '$push': {"comentarios": { "texto_comentario" : request.json["texto_comentario"], "autor_comentario" : request.json["autor_comentario"]}}})
        getAllHilos(db)
        return jsonify({'RESULTADO': "Bien"}), 200
    else: 
        return jsonify({'RESULTADO': 'Faltan datos'}), 400

@application.route('/hilo/comentarios', methods=['DELETE'])
@auth_required
def deleteComentarioHilo(user, id):
    isComentario = "texto_comentario" in request.json
    isAutorC = "autor_comentario" in request.json
    isHilo = "titulo_hilo" in request.json
    isAutorH = "autor_hilo" in request.json
    if isComentario and isAutorC and isHilo and isAutorH:
        db.hilos.update_one({"titulo_hilo":request.json["titulo_hilo"],"autor_hilo":request.json["autor_hilo"]}, {
                    '$pull': {"comentarios": { "texto_comentario" : request.json["texto_comentario"], "autor_comentario" : request.json["autor_comentario"]}}},False,True)
        getAllHilos(db)
        return jsonify({'RESULTADO': "Bien"}), 200
    else: 
        return jsonify({'RESULTADO': 'Faltan datos'}), 400

@application.errorhandler(401)
def unauthorized(e):
    return jsonify({'Error': 'No estas autenticado'}), 401


def getAllHilos(db):
    _hilos = []
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


def getUserName(users, username):
    for user in users:
        if user.getUser() == username:
            return user.getName()
    return "Anonimo"


if __name__ == '__main__':
    getAllUsers(db)
    getAllHilos(db)
    application.run(debug=True)
