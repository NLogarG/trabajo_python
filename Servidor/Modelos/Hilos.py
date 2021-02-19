from flask.json import dump
from Modelos.Comentarios import Comentario


class Hilo:

    def __init__(self, datos_hilo):
        comentarios = []
        _comentarios = []
        self.autor_hilo = datos_hilo["autor_hilo"]
        self.titulo_hilo = datos_hilo["titulo_hilo"]
        isComentarios = 'comentarios' in datos_hilo
        if isComentarios:
            self.tienecoments= True
            _comentarios = datos_hilo["comentarios"]
            for _comentario in _comentarios:
                comentarios.append(Comentario(_comentario))
            self.comentarios = comentarios
        else:
            self.tienecoments = False

    def getTitulo(self):
        return self.titulo_hilo

    def getAutor(self):
        return self.autor_hilo

    def haveComentarios(self):
        return self.tienecoments

    def getComentarios(self):
        _listacomentarios = []
        for _comentario in self.comentarios:
            _listacomentarios.append([_comentario.getTexto(),_comentario.getAutor()])
        return _listacomentarios
