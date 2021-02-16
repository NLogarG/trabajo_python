import json
import requests

hilos = []
cuenta_hilos = 0

def getNumber(min,max,texto):
    print(cuenta_hilos)
    if max == -1:
        max= cuenta_hilos
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
        'password': encriptar(passs),     
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
        titulos_hilo = str(_hilos['RESULTADO'])
        orden = 101
        hilos.clear
        for hilo in titulos_hilo.split(','):
            print("["+str(orden)+"] "+hilo)
            hilos.append(hilo)
            orden +=1
        cuenta_hilos = orden

def setHilo(autor_hilo,titulo_hilo,token):
    header = {
        'Content-Type': 'application/json',
        'Authorization': token,
    }
    datos_hilo = {
        'titulo_hilo': titulo_hilo,  
        'autor_hilo': autor_hilo,   
        'comentarios': ""
    }
    response = requests.post('http://127.0.0.1:5000/hilo', json=datos_hilo,headers=header)
    if response.status_code == 200:
        print("Hilo registrado")
    else:
        print("Fallo al crear Hilo")

def deleteHilo(id_hilo, token):
    header = {
        'Content-Type': 'application/json',
        'Authorization': token,
    }
    datos_hilo = {
        'titulo_hilo': hilos[id_hilo-101],
    }
    response = requests.delete('http://127.0.0.1:5000/hilo', json=datos_hilo,headers=header)
    if response.status_code == 200:
        print("Hilo borrado")
    else:
        print("Fallo al borrar Hilo")

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
