from typing import List, Dict, Any
import reflex as rx
from BookWorms.models.dbbroker import DBBroker

class SearchState(rx.State):
    query: str = ""
    resultados: List[Dict[str, Any]] = []  # ← ahora es un Var tipado


    def buscar(self):
        db = DBBroker()
        if self.query.startswith("@"):
            datos = db.buscar_usuarios(self.query[1:])
        else:
            datos = db.buscar_libros(self.query)
        self.resultados = datos or []

    def search_and_redirect(self):
        self.buscar()
        return rx.redirect("/search")