class Comentario:

    def __init__ (self,datos_comentario):
        self.texto_comentario = datos_comentario["texto_comentario"]
        self.autor_comentario = datos_comentario["autor_comentario"]
    
    def getTexto(self):
        return self.texto_comentario

    def getAutor(self):
        return self.autor_comentario