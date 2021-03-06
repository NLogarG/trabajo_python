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
    os.system("cls")
    while no_menu:
        print("  ______________________  ")
        print("||                      ||")
        print("||    MENU PRINCIPAL    ||")
        print("||                      ||")
        print("||      [1] Login       ||")
        print("||   [2] Crear Cuenta   ||")
        print("||    [3] Ver hilos     ||")
        print("||      [0] Salir       ||")
        print("||                      ||")
        print("||______________________||")
        opcion = utils.getNumber(0, 4, "Opción: ")
        if opcion == 1:
            os.system("cls")
            print("{### FORMULARIO LOGEO ###}")
            user = input("Usuario: ")
            passs = utils.keyAlmacenada(0,user,"")
            no_guardado = False
            if passs == None:
                no_guardado = True
                passs = input("Contraseña: ")
            token = utils.getToken(user, passs)
            if token != False:
                if no_guardado:
                    utils.keyAlmacenada(1,user,passs)
                name = utils.getName(token)
                no_menu2 = True
                while no_menu2:
                    if primera_vez:
                        os.system("cls")
                        print("Bienvenido " + name)
                        primera_vez = False
                    maxima = 2
                    os.system("cls")
                    print("  ______________________  ")
                    print("||                      ||")
                    print("||        LOGEADO       ||")
                    print("||                      ||")
                    print("||    [1] Ver hilos     ||")
                    if user != "Anonimo":
                        print("||    [2] Nuevo hilo    ||")                        
                        maxima = 3
                        if name == "dios":
                            print("||    [3] Borrar hilo   ||")                            
                            maxima = 4
                    print("||       [0] Salir      ||")
                    print("||                      ||")
                    print("||______________________||")
                    opcion = utils.getNumber(0, maxima, "Opción: ")
                    if opcion == 1:
                        no_menu21 = True
                        while no_menu21:
                            os.system("cls")
                            print("  ______________________________________________  ")
                            print("||\t\t\t\t\t\t||")
                            print("||\t\tSELECCIONA EL HILO\t\t||")
                            utils.getHilos()
                            print("||\t\t[100] Volver\t\t\t||")
                            print("||\t\t\t\t\t\t||")
                            print("||______________________________________________||")
                            opcion = utils.getNumber(
                                100, utils.cuenta_hilos, "ID Hilo: ")
                            if opcion >= 101:
                                no_menu4 = True
                                while no_menu4:
                                    os.system("cls")
                                    print("Mostrando hilo " + str(opcion) +
                                          ": "+utils.hilos[opcion-101])
                                    print("  _______________________________________________________________________________  ") 
                                    print("||\t\t\t\t\t\t\t\t\t\t||")
                                    print("||\t\t\t\t\tHILOS\t\t\t\t\t||")                                
                                    utils.getComentarios(opcion)
                                    if (name == "dios"):
                                        print("||\t\t\t\t[98] Borrar comentario\t\t\t\t||")                                                                                                                       
                                    if (name != "Anonimo"):
                                        print("||\t\t\t\t[99] Añadir comentario\t\t\t\t||")                                         
                                    print("||\t\t\t\t\t\t\t\t\t\t||")                                         
                                    print("||\t\t\t\t[100] Volver\t\t\t\t\t||")
                                    print("||\t\t\t\t\t\t\t\t\t\t||") 
                                    print("||______________________________________________________________________________||")
                                    opcion2 = utils.getNumber(
                                        98, 101, "Opcion: ")
                                    if opcion2 == 100:
                                        no_menu4 = False
                                        os.system("cls")
                                    elif opcion2 == 99:
                                        print("{### NUEVO COMENTARIO ###}")
                                        texto_comentario = input("Texto del comentario: ")
                                        utils.setComentarioHilo(opcion,texto_comentario,name,token)
                                    elif opcion2 == 98:
                                        print("{### BORRAR COMENTARIO ###}")
                                        Id_comentario = utils.getNumber(100,utils.cuenta_comentarios,"Id Comentario: ")
                                        utils.deleteComentarioHilo(opcion,Id_comentario,token)
                            else:
                                no_menu21 = False
                                os.system("cls")
                    elif opcion == 2:
                        os.system("cls")
                        print("Escribe 'Cancelar' para cancelar la accion.")
                        print("{########~NUEVO HILO~########}")
                        titulo_hilo = input("Nombre del hilo: ")
                        if titulo_hilo != "Cancelar":
                            utils.setHilo(name, titulo_hilo, token)
                    elif opcion == 3:
                        os.system("cls")
                        print("  ______________________________________________")
                        print("||\t\t\t\t\t\t||")
                        print("||\t\tSELECCIONA EL HILO\t\t||")
                        utils.getHilos()
                        print("||\t\t\t\t\t\t||")
                        print("||\t\t[100] Volver\t\t\t||")
                        print("||\t\t\t\t\t\t||")
                        print("||______________________________________________||")
                       
                        id_hilo = utils.getNumber(
                            100, utils.cuenta_hilos, "ID Hilo: ")
                        if id_hilo != 100:
                            utils.deleteHilo(id_hilo, token)
                    else:
                        no_menu2 = False
                        os.system("cls")
                        primera_vez = True
                        name = "Anonimo"
                        token = False
            else:
                print("Usuario/Contraseña Incorrectos")

        elif opcion == 2:
            no_pass = True
            os.system("cls")
            print("{### FORMULARIO REGISTRO ###}")
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
                print("  ______________________________________________  ")
                print("||\t\t\t\t\t\t||")
                print("||\t\tSELECCIONA EL HILO\t\t||")
                utils.getHilos()
                print("||\t\t\t\t\t\t||")
                print("||\t\t[100] Volver\t\t\t||")
                print("||______________________________________________||")
                opcion = utils.getNumber(100, utils.cuenta_hilos, "Opción: ")
                if opcion != 100:
                    no_menu31 = True
                    while no_menu31:
                        os.system("cls")                        
                        print("Mostrando hilo " + str(opcion) +
                              ": "+utils.hilos[opcion-101])
                        print("  _______________________________________________________________________________  ") 
                        print("||\t\t\t\t\t\t\t\t\t\t||")
                        print("||\t\t\t\t\tHILOS\t\t\t\t\t||")      
                        utils.getComentarios(opcion)
                        print("||\t\t\t\t\t\t\t\t\t\t||") 
                        print("||\t\t\t\t[100] Volver\t\t\t\t\t||")
                        print("||\t\t\t\t\t\t\t\t\t\t||")
                        print("||______________________________________________________________________________||")                        
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
