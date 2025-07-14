import reflex as rx
from BookWorms.models.dbbroker import DBBroker


class ABLibroState(rx.State):
    modo: str = "Alta"
    titulo: str
    isbn: str
    autor: str
    editorial: str
    sinopsis: str

    def set_modo(self, value: str):
        self.modo = value

    def ejecutar_accion(self):
        db = DBBroker()

        if self.modo == "Alta":
            db.alta_libro(titulo=self.titulo, isbn=self.isbn, autor=self.autor, editorial=self.editorial,
                          sinopsis=self.sinopsis)
        elif self.modo == "Baja":
            db.baja_libro(isbn=self.isbn)

        return rx.redirect("/feed")
