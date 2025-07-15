import reflex as rx
from BookWorms.models.dbbroker import DBBroker
import json


class ReportesState(rx.State):
    # Reporte que acaba de seleccionar el usuario
    selected_report: str = ""
    report_data:     list[dict] = []

    @rx.event
    def load_libros_leidos(self):
        data = DBBroker().reporte_libros_mas_leidos()
        self.report_data = data

    @rx.event
    def load_libros_por_leer(self):
        data = DBBroker().reporte_libros_por_leer()
        self.report_data = data

    @rx.event
    def load_usuarios_seguidos(self):
        data = DBBroker().reporte_usuarios_seguidos()
        self.report_data = data
