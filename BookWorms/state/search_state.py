from typing import List, Dict, Any
import reflex as rx
from postgrest import APIError

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

        # """Estado para búsqueda de libros por título."""
        # query: str = ""
        # results: list = []

    def set_query(self, value: str) -> None:
        """Actualiza el término de búsqueda."""
        self.query = value

    def search_books(self) -> None:
        """Realiza la búsqueda de libros cuyo título contenga el query."""
        broker = DBBroker().supabase
        try:
            resp = (
                broker
                .from_("libros")
                .select("*")
                .ilike("titulo", f"%{self.query}%")
                .execute()
            )
            self.resultados = resp.data or []
        except APIError as e:
            print("Error al buscar libros:", e)

    def clear_results(self) -> None:
        """Vacía la lista de resultados."""
        self.resultados = []

    def clear_search(self) -> None:
        """Resetea el query y los resultados de búsqueda."""
        self.query = ""
        self.resultados = []
