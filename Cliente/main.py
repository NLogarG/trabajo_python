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
                print("Bienvenido " + utils.getName(token))
                no_menu = False
            else:
                print("Usuario/Contraseña Incorrectos")
        elif opcion == 2:
            user = input("Usuario: ")
            passs = input("Contraseña: ")
            name = input("Nombre: ")
            utils.Logon(user,passs,name)
        elif opcion == 3:
            print("Mostrar hilos")
        elif opcion == 0:
            print("Saliendo...")
            no_menu = False


menu()
