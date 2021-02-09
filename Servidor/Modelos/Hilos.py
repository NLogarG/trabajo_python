from Comentarios import Comentario
class Hilo:

    def __init__ (self,datos_hilo):
        comentarios = []
        _comentarios = []
        self.titulo_hilo = datos_hilo["titulo_hilo"]
        _comentarios = datos_hilo["comentarios_hilo"]
        for _comentario in _comentarios:
            comentarios.append(Comentario(_comentario))
        self.comentarios = comentarios



