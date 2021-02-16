import utils

token = False
name = "Anonimo"

def menu():
    no_menu = True
    while no_menu:
        print("[1] Login")
        print("[2] Crear Cuenta")
        print("[3] Ver hilos")
        print("[0] Salir")
        opcion = utils.getNumber(0,4,"Opción: ")
        if opcion == 1:
            user = input("Usuario: ")
            passs = input("Contraseña: ")
            token = utils.getToken(user, passs)
            if token != False:
                name = utils.getName(token)            
                no_menu2 = True
                while no_menu2:
                    print("Bienvenido " + name)
                    maxima = 2
                    print("[1] Ver hilos")
                    if user != "Anonimo":
                        print("[2] Nuevo hilo")                        
                        maxima = 3
                        if name == "dios":
                            print("[3] Borrar hilo")
                            maxima = 4
                    print("[0] Salir")
                    opcion = utils.getNumber(0,maxima,"Opción: ")
                    if opcion == 1:
                        no_menu21 = True
                        while no_menu21:
                            utils.getHilos()
                            print("[0] Volver")
                            opcion = utils.getNumber(0,utils.cuenta_hilos,"ID Hilo: ")
                            if opcion >= 101 and opcion < utils.cuenta_hilos:
                                 
                            elif opcion == 0 :
                                no_menu21 = False
                    elif opcion == 2:
                        titulo_hilo = input("Nombre del hilo: ")
                        utils.setHilo(name,titulo_hilo,token)
                    elif opcion ==3:
                        utils.getHilos()
                        id_hilo = utils.getNumber(101,utils.cuenta_hilos,"ID Hilo: ")
                        utils.deleteHilo(id_hilo,token)
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
            print("Registrandose como ANONIMO")
            utils.getHilos()
            no_menu3 = True
            while no_menu3:
                print("[0] Salir")
                opcion = utils.getNumber(0,utils.cuenta_hilos,"ID Hilo: ")
                if opcion == 1:
                    print("Introduzca el ID del hilo: ")                        
                elif opcion == 0:
                    print("Saliendo al menu principal...")
                    no_menu3 = False







        elif opcion == 0:
            print("Saliendo...")
            no_menu = False


menu()
