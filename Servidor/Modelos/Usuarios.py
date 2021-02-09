import hashlib

class User:

    def __init__(self,datos_user):
        self.user = datos_user['user']
        self.password = datos_user['password']
        self.name = datos_user['name']

    def getName(self):
        return self.name

    def getUser(self):
        return self.user

    def getPassword(self):
        contraseña = ""
        for c in self.password:
            if c.isupper(): 
                c_index = ord(c) - ord('A')
                c_og_pos = (c_index - 6) % 26 + ord('A')
                c_og = chr(c_og_pos)
                contraseña += c_og
            elif c.islower(): 
                c_index = ord(c) - ord('a') 
                c_og_pos = (c_index - 6) % 26 + ord('a')
                c_og = chr(c_og_pos)
                contraseña += c_og
            elif c.isdigit():
                c_og = (int(c) - 6) % 10
                contraseña += str(c_og)
            else:
                contraseña += c
        return contraseña