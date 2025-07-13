from typing import List, Dict, Any
import reflex as rx
from BookWorms.models.dbbroker import DBBroker


class AmigosState(rx.State):
    query: str = ""
    resultados: List[Dict[str, Any]] = []  # ← ahora es un Var tipado

    def get_friends(self):
        db = DBBroker()
        username = db.get_last_current_user()
        user_id = db.get_user_by_username(str(username))[0]['id']
        datos = db.get_amigos_from_user_id(user_id)
        self.resultados = [{"username": d} for d in datos] if datos else []
        del db

        """
        if type(user_id) is not None:
            datos = db.get_amigos_from_user_id(str(user_id))
            self.resultados = datos
        else:
            self.resultados = []"""

    def get_friends_and_redirect(self):
        self.get_friends()
        return rx.redirect("/amigos")

    def get_current_user_id(self):
        db = DBBroker()
        username = db.get_last_current_user()
        user = db.get_user_by_username(str(username))
        del db
        return user[0]['id'] if user else None

    def eliminar_amigo(self, user_id, amigo_id):
        db = DBBroker()
        db.eliminar_amigo(user_id, amigo_id)
        del db
        # Refresh the friends list after deletion
        return self.get_friends_and_redirect()

