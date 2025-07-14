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

    @staticmethod
    def get_current_user_id(db):
        return db.get_user_by_username(str(db.get_last_current_user()))[0]['id']

    def eliminar_amigo(self, amigo_username: str):
        db = DBBroker()
        current_user_id = AmigosState.get_current_user_id(db)
        amigo_id = db.get_user_by_username(str(amigo_username))[0]['id']
        db.eliminar_amigo(current_user_id, amigo_id)

        del db
        return self.get_friends_and_redirect()

    def agregar_amigo(self, amigo_username: str):
        db = DBBroker()
        current_user_id = AmigosState.get_current_user_id(db)
        amigo_id = db.get_user_by_username(str(amigo_username))[0]['id']
        db.agregar_amigo(current_user_id, amigo_id)

        del db
        return self.get_friends_and_redirect()
