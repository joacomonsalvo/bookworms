class Publicacion:
    def __init__(self, ID, fecha, titulo, texto, comentarios, likes, linked_user_id):
        self.ID = ID
        self.fecha = fecha
        self.titulo = titulo
        self.texto = texto
        self.comentarios = comentarios
        self.likes = likes
        self.linked_user_id = linked_user_id

    def nuevo_comentario(self):
        pass

    def eliminar_comentario(self):
        pass

    def alta_like(self):
        pass

    def baja_like(self):
        pass
