import json
from logging import raiseExceptions
import requests
import keyring

hilos = []
autorHilos = []
comentarios = []
autorComentarios = []
cuenta_hilos = 0
cuenta_comentarios = 0


def getNumber(min, max, texto):
    numeros_bien = True
    opcion = 0
    while numeros_bien:
        try:
            opcion = int(input(texto))
            if opcion >= min and opcion < max:
                numeros_bien = False
            else:
                print("Selecciona opcion valida.")
        except ValueError:
            print("Selecciona opcion valida.")
    return opcion


def getToken(user, passs):
    respuesta = []
    datos_user = {
        'usuario': user,
        'password': passs,
    }
    response = requests.post('http://127.0.0.1:5000/login', json=datos_user)
    if response.status_code == 200:
        respuesta = response.json()
        token = respuesta['RESULTADO']
        return token
    else:
        respuesta = response.json()
        print(respuesta['RESULTADO'])
        return False


def getName(token):
    nombre = []
    header = {
        'Content-Type': 'application/json',
        'Authorization': token,
    }
    response = requests.get('http://127.0.0.1:5000/datos', headers=header)
    if response.status_code == 200:
        nombre = response.json()
        return nombre['datos']
    return response


def Logon(user, passs, name):
    datos_user = {
        'usuario': user,
        'password': passs,
        'name': name
    }
    response = requests.post('http://127.0.0.1:5000/logon', json=datos_user)
    if response.status_code == 200:
        print("Usuario registrado")
    else:
        print("Fallo al crear Usuario")


def getHilos():
    global cuenta_hilos
    _hilos = []
    response = requests.get('http://127.0.0.1:5000/hilos')
    if response.status_code == 200:
        _hilos = response.json()
        titulos_hilo = str(_hilos['Hilos'])
        autores_hilo = str(_hilos['Autores'])
        orden = 101
        hilos.clear
        for hilo in titulos_hilo.split(','):
            tabulaciones = ""
            if len(hilo) <= 7:
                tabulaciones = "\t\t\t\t\t"
            elif len(hilo) <= 15:
                tabulaciones = "\t\t\t\t"
            elif len(hilo) <= 23:
                tabulaciones = "\t\t\t"
            elif len(hilo) <= 31:
                tabulaciones = "\t\t"
            elif len(hilo) <= 39:
                tabulaciones = "\t"
            else:
                tabulaciones = ""
            print("|| ["+str(orden)+"] " + hilo + tabulaciones + "||")
            hilos.append(hilo)
            orden += 1
        for hilo in autores_hilo.split(','):
            autorHilos.append(hilo)
        cuenta_hilos = orden
        if cuenta_hilos == 0:
            cuenta_hilos = 101


def setHilo(autor_hilo, titulo_hilo, token):
    header = {
        'Content-Type': 'application/json',
        'Authorization': token,
    }
    datos_hilo = {
        'titulo_hilo': titulo_hilo,
        'autor_hilo': autor_hilo
    }
    response = requests.post('http://127.0.0.1:5000/hilo',
                             json=datos_hilo, headers=header)
    if response.status_code == 200:
        print("Hilo registrado")
    else:
        print("Fallo al crear hilo")


def deleteHilo(id_hilo, token):
    header = {
        'Content-Type': 'application/json',
        'Authorization': token,
    }
    datos_hilo = {
        'titulo_hilo': hilos[id_hilo-101],
    }
    response = requests.delete(
        'http://127.0.0.1:5000/hilo', json=datos_hilo, headers=header)
    if response.status_code == 200:
        print("Hilo borrado")
    else:
        print("Fallo al borrar Hilo")


def getComentarios(id_hilo):
    global cuenta_comentarios
    strcomentarios = ""
    _comentarios = []
    comentario = []
    datos_hilo = {
        'titulo_hilo': hilos[id_hilo-101],
    }
    response = requests.get(
        'http://127.0.0.1:5000/hilo/comentarios', json=datos_hilo)
    if response.status_code == 200:
        _comentarios = response.json()
        strcomentarios = _comentarios["RESULTADO"]
        orden = 101
        _comentarios = strcomentarios.split(";")
        for _comentario in _comentarios:            
            comentario = _comentario.split(",")
            comentarios.append(comentario[0])
            autorComentarios.append(comentario[1])
            tabulaciones = ""
            if len(comentario[0]) <= 7:
                tabulaciones = "\t\t\t\t\t\t"
            elif len(comentario[0]) <= 15:
                tabulaciones = "\t\t\t\t\t"
            elif len(comentario[0]) <= 23:
                tabulaciones = "\t\t\t\t"
            elif len(comentario[0]) <= 31:
                tabulaciones = "\t\t\t"
            elif len(comentario[0]) <= 39:
                tabulaciones = "\t\t"
            elif len(comentario[0]) <= 47:
                tabulaciones = "\t"
            else:
                tabulaciones = ""
            print("|| ["+str(orden)+"] Texto: " + comentario[0] +
                  tabulaciones + "Autor: " +comentario[1] + "\t||")
            orden += 1
        cuenta_comentarios = orden
        if cuenta_comentarios == 0:
            cuenta_comentarios = 101
    elif response.status_code == 201:
        respuesta = []
        respuesta = response.json()
        print("||\t\t\t\t"+respuesta["RESULTADO"]+"\t\t\t\t||")
    else:
        print("Fallo al buscar Comentarios Codigo: "+response.status_code)


def setComentarioHilo(id_hilo,texto_comentario,autor_comentario,token):
    header = {
        'Content-Type': 'application/json',
        'Authorization': token,
    }
    datos_hilo = {
        'titulo_hilo': hilos[id_hilo-101],
        'autor_hilo' : autorHilos[id_hilo-101],
        'texto_comentario' : texto_comentario,
        'autor_comentario' : autor_comentario
    }
    response = requests.put(
        'http://127.0.0.1:5000/hilo/comentarios', json=datos_hilo,headers=header)
    if response.status_code == 200:
        print("Comentario añadido.")

def deleteComentarioHilo(id_hilo,id_comentario,token):
    header = {
        'Content-Type': 'application/json',
        'Authorization': token,
    }
    datos_hilo = {
        'titulo_hilo': hilos[id_hilo-101],
        'autor_hilo' : autorHilos[id_hilo-101],
        'texto_comentario' : comentarios[id_comentario-100],
        'autor_comentario' : autorComentarios[id_comentario-100]
    }
    response = requests.delete(
        'http://127.0.0.1:5000/hilo/comentarios', json=datos_hilo,headers=header)
    if response.status_code == 200:
        print("Comentario borrado.")

def keyAlmacenada(estado,nombre,contraseña):
    if estado == 0:
        if keyring.get_password("Foro Python",nombre) != None:
            print("¿Deseas iniciar sesion automaticamente?\n[0] No\t[1] Si")
            numero = getNumber(0,2,"Opcion: ")
            if numero == 1:
                return keyring.get_password("Foro Python",nombre)
        return None
    elif estado == 1:
        print("¿Deseas guardar las credenciales?\n[0] No\t[1] Si")
        numero = getNumber(0,2,"Opcion: ")
        if numero == 1:
            keyring.set_password("Foro Python",nombre,contraseña)
            print("Credenciales guardadas.")


def encriptar(plain_text):
    encriptado = ""
    for c in plain_text:
        if c.isupper():
            c_index = ord(c) - ord('A')
            c_shifted = (c_index + 6) % 26 + ord('A')
            c_new = chr(c_shifted)
            encriptado += c_new
        elif c.islower():
            c_index = ord(c) - ord('a')
            c_shifted = (c_index + 6) % 26 + ord('a')
            c_new = chr(c_shifted)
            encriptado += c_new
        elif c.isdigit():
            c_new = (int(c) + 6) % 10
            encriptado += str(c_new)
        else:
            encriptado += c
    return encriptado
