from Modelos.Comentarios import Comentario


class Hilo:

    def __init__(self, datos_hilo):
        comentarios = []
        _comentarios = []
        self.autor_hilo = datos_hilo["autor_hilo"]
        self.titulo_hilo = datos_hilo["titulo_hilo"]
        isComentarios = 'comentarios' in datos_hilo
        if isComentarios:
            _comentarios = datos_hilo["comentarios"]
            for _comentario in _comentarios:
                comentarios.append(Comentario(_comentario))
            self.comentarios = comentarios

    def getTitulo(self):
        return self.titulo_hilo

    def getComentarios(self):
        return self.comentarios
