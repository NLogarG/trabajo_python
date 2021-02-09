import utils

token = False


def menu():
    no_menu = True
    while no_menu:
        print("[1] Login")
        print("[2] Crear Cuenta")
        print("[3] Ver hilos")
        print("[0] Salir")
        opcion = utils.getNumber(4)
        if opcion == 1:
            user = input("Usuario: ")
            passs = input("Contraseña: ")
            token = utils.getToken(user, passs)
            if token != False:                
                no_menu2 = True
                while no_menu2:
                    print("Bienvenido " + utils.getName(token))
                    maxima = 2
                    print("[1] Ver hilos")
                    if user != "Anonimo":
                        print("[2] Nuevo hilo")
                        maxima = 3
                        if user == "Admin":
                            print("[3] Borrar hilo")
                            maxima = 4
                    print("[0] Salir")
                    opcion = utils.getNumber(maxima)
                    if opcion == 1:
                        print("Hilos...")
                    elif opcion == 2:
                        print("Creando hilo...")
                    else:
                        no_menu2 = False
            else:            
                print("Usuario/Contraseña Incorrectos")
        elif opcion == 2:
            no_pass = True
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
            print("Mostrar hilos")
        elif opcion == 0:
            print("Saliendo...")
            no_menu = False


menu()
