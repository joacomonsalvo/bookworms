import reflex as rx
from BookWorms.models.dbbroker import DBBroker

class SearchState(rx.State):
    query: str = ""
    resultados: list = []

    def buscar(self):
        db = DBBroker()
        print("⚙️ SearchState.buscar – query actual:", self.query)
        if self.query.startswith("@"):
            username = self.query[1:]
            self.resultados = db.buscar_usuarios(username)
        else:
            self.resultados = db.buscar_libros(self.query)
