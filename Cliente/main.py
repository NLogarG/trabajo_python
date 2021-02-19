import utils
import os

global token
global name
global primera_vez


def menu():
    primera_vez = True
    name = "Anonimo"
    no_menu = True
    token = False
    while no_menu:
        print("[1] Login")
        print("[2] Crear Cuenta")
        print("[3] Ver hilos")
        print("[0] Salir")
        opcion = utils.getNumber(0, 4, "Opción: ")
        if opcion == 1:
            os.system("cls")
            user = input("Usuario: ")
            passs = input("Contraseña: ")
            token = utils.getToken(user, passs)
            if token != False:
                name = utils.getName(token)
                no_menu2 = True
                while no_menu2:
                    if primera_vez:
                        os.system("cls")
                        print("Bienvenido " + name)
                        primera_vez = False
                    maxima = 2
                    os.system("cls")
                    print("[1] Ver hilos")
                    if user != "Anonimo":
                        print("[2] Nuevo hilo")
                        maxima = 3
                        if name == "dios":
                            print("[3] Borrar hilo")
                            maxima = 4
                    print("[0] Salir")
                    opcion = utils.getNumber(0, maxima, "Opción: ")
                    if opcion == 1:
                        no_menu21 = True
                        while no_menu21:
                            utils.getHilos()
                            print("[100] Volver")
                            opcion = utils.getNumber(
                                100, utils.cuenta_hilos, "ID Hilo: ")
                            if opcion >= 101:
                                no_menu4 = True
                                while no_menu4:                                
                                    os.system("cls")
                                    print("Mostrando hilo " + str(opcion) +
                                    ": "+utils.hilos[opcion-101])
                                    print("COMENTARIOS")
                                    utils.getComentarios(opcion) 
                                    print("[100] Volver")
                                    opcion = utils.getNumber(100, 101, "Opcion: ")      
                                    if opcion == 100:
                                        no_menu4 = False

                            else:
                                no_menu21 = False
                    elif opcion == 2:
                        os.system("cls")
                        print("Escribe 'Cancelar' para cancelar la accion.")
                        titulo_hilo = input("Nombre del hilo: ")
                        if titulo_hilo != "Cancelar":
                            utils.setHilo(name, titulo_hilo, token)
                    elif opcion == 3:
                        os.system("cls")
                        utils.getHilos()
                        print("[100] Cancelar")
                        id_hilo = utils.getNumber(
                            100, utils.cuenta_hilos, "ID Hilo: ")
                        if id_hilo != 100:
                            utils.deleteHilo(id_hilo, token)
                    else:
                        no_menu2 = False
                        primera_vez = True
                        name = "Anonimo"
                        token = False
            else:
                print("Usuario/Contraseña Incorrectos")

        elif opcion == 2:
            no_pass = True
            os.system("cls")
            user = input("Usuario: ")
            while no_pass:
                passs = input("Contraseña: ")
                repass = input("Introduzca de nuevo la contraseña: ")
                if passs == repass:
                    no_pass = False
                else:
                    print("Las contraseñas no coinciden")                    
            name = input("Nombre: ")
            utils.Logon(user, passs, name)

        elif opcion == 3:
            if primera_vez:
                os.system("cls")
                print("Has entrado como " + name)
                primera_vez = False
            no_menu3 = True
            while no_menu3:
                utils.getHilos()
                print("[100] Salir")
                opcion = utils.getNumber(100, utils.cuenta_hilos, "Opción: ")
                if opcion != 100:
                    no_menu31 = True
                    while no_menu31:
                        os.system("cls")
                        print("Mostrando hilo " + str(opcion) +
                              ": "+utils.hilos[opcion-101])
                        utils.getComentarios(opcion)
                        print("[100] Volver")
                        opcion = utils.getNumber(100, 101, "Opción: ")
                        if opcion == 100:
                            os.system("cls")
                            no_menu31 = False
                else:
                    os.system("cls")
                    no_menu3 = False
                    primera_vez = True
                    name = "Anonimo"

        elif opcion == 0:
            os.system("cls")
            print("Saliendo...")
            no_menu = False


menu()
