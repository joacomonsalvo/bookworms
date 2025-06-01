from views.base_html import *
from models.lista_privada import ListaPrivada
from models.usuario import Usuario

class ListasPrivadasView:
    """Vista para gestión de listas privadas del usuario"""
    
    def __init__(self):
        pass
    
    def render(self, usuario_id: str, mensaje: str = None) -> str:
        """Renderizar página de listas privadas"""
        try:
            # Obtener listas privadas del usuario
            listas = ListaPrivada.obtener_por_usuario_privadas(usuario_id)
            usuario = Usuario.obtener_por_id(usuario_id)
            
            page = HTMLPage("Mis Listas Privadas")
            
            # Navbar
            navbar = Navbar(usuario.username if usuario else "Usuario")
            page.add_component(navbar)
            
            # Contenedor principal
            container = Div(css_class="container mx-auto px-4 py-8")
            
            # Header con botón para crear nueva lista
            header = Div(css_class="flex justify-between items-center mb-8")
            header.add_component(H1("Mis Listas Privadas", css_class="text-3xl font-bold text-gray-800"))
            
            # Botón crear nueva lista
            btn_nueva = Button(
                "Nueva Lista Privada",
                css_class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg",
                onclick="mostrarModalNuevaLista()"
            )
            header.add_component(btn_nueva)
            container.add_component(header)
            
            # Mensaje de feedback
            if mensaje:
                alert = Div(mensaje, css_class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6")
                container.add_component(alert)
            
            # Grid de listas
            if listas:
                grid = Div(css_class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6")
                
                for lista in listas:
                    stats = lista.obtener_estadisticas()
                    
                    # Card de lista
                    card = Card()
                    
                    # Header de la card
                    card_header = Div(css_class="flex justify-between items-start mb-4")
                    card_header.add_component(H3(lista.nombre, css_class="text-xl font-semibold text-gray-800"))
                    
                    # Badge de privacidad
                    privacy_badge = Span(
                        lista.nivel_privacidad.title(),
                        css_class=f"px-2 py-1 text-xs rounded-full {'bg-red-100 text-red-800' if lista.nivel_privacidad == 'privada' else 'bg-yellow-100 text-yellow-800'}"
                    )
                    card_header.add_component(privacy_badge)
                    card.add_component(card_header)
                    
                    # Descripción
                    if lista.descripcion:
                        card.add_component(P(lista.descripcion[:100] + "..." if len(lista.descripcion) > 100 else lista.descripcion, 
                                           css_class="text-gray-600 mb-4"))
                    
                    # Estadísticas
                    stats_div = Div(css_class="grid grid-cols-2 gap-4 mb-4 text-sm")
                    stats_div.add_component(Div([
                        Span("Total libros: ", css_class="font-medium"),
                        Span(str(stats['total_libros']))
                    ]))
                    stats_div.add_component(Div([
                        Span("Leídos: ", css_class="font-medium"),
                        Span(str(stats['libros_leidos']))
                    ]))
                    stats_div.add_component(Div([
                        Span("Leyendo: ", css_class="font-medium"),
                        Span(str(stats['libros_leyendo']))
                    ]))
                    stats_div.add_component(Div([
                        Span("Por leer: ", css_class="font-medium"),
                        Span(str(stats['libros_quiero_leer']))
                    ]))
                    card.add_component(stats_div)
                    
                    # Progreso del objetivo (si existe)
                    if lista.objetivo_lectura:
                        progreso = lista.actualizar_progreso_objetivo()
                        if progreso:
                            progress_div = Div(css_class="mb-4")
                            progress_div.add_component(P(f"Objetivo: {progreso['objetivo']} {lista.objetivo_lectura['tipo']}", 
                                                       css_class="text-sm font-medium mb-1"))
                            
                            # Barra de progreso
                            progress_bar = Div(css_class="w-full bg-gray-200 rounded-full h-2")
                            progress_fill = Div(
                                css_class=f"bg-blue-600 h-2 rounded-full",
                                style=f"width: {progreso['porcentaje']}%"
                            )
                            progress_bar.add_component(progress_fill)
                            progress_div.add_component(progress_bar)
                            progress_div.add_component(P(f"{progreso['progreso']}/{progreso['objetivo']} ({progreso['porcentaje']:.1f}%)", 
                                                       css_class="text-xs text-gray-600 mt-1"))
                            card.add_component(progress_div)
                    
                    # Botones de acción
                    actions = Div(css_class="flex gap-2")
                    actions.add_component(Button("Ver", 
                                                css_class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded text-sm",
                                                onclick=f"window.location.href='/lista/{lista.lista_id}'"))
                    actions.add_component(Button("Editar", 
                                                css_class="flex-1 bg-gray-600 hover:bg-gray-700 text-white py-2 px-4 rounded text-sm",
                                                onclick=f"editarLista('{lista.lista_id}')"))
                    card.add_component(actions)
                    
                    grid.add_component(card)
                
                container.add_component(grid)
            else:
                # Estado vacío
                empty_state = Div(css_class="text-center py-12")
                empty_state.add_component(H3("No tienes listas privadas", css_class="text-xl text-gray-600 mb-4"))
                empty_state.add_component(P("Crea tu primera lista para organizar tus libros", css_class="text-gray-500 mb-6"))
                empty_state.add_component(Button("Crear Primera Lista", 
                                                css_class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg",
                                                onclick="mostrarModalNuevaLista()"))
                container.add_component(empty_state)
            
            page.add_component(container)
            
            # Modal para nueva lista
            modal = self._crear_modal_nueva_lista()
            page.add_component(modal)
            
            # JavaScript
            js_code = """
            function mostrarModalNuevaLista() {
                document.getElementById('modalNuevaLista').classList.remove('hidden');
            }
            
            function cerrarModal() {
                document.getElementById('modalNuevaLista').classList.add('hidden');
            }
            
            function editarLista(listaId) {
                window.location.href = '/lista/' + listaId + '/editar';
            }
            """
            page.add_script(js_code)
            
            return page.render()
            
        except Exception as e:
            print(f"Error renderizando listas privadas: {e}")
            return self._render_error("Error cargando listas privadas")
    
    def _crear_modal_nueva_lista(self) -> Div:
        """Crear modal para nueva lista"""
        modal = Div(css_class="fixed inset-0 bg-black bg-opacity-50 hidden z-50", id="modalNuevaLista")
        
        modal_content = Div(css_class="flex items-center justify-center min-h-screen p-4")
        modal_dialog = Div(css_class="bg-white rounded-lg max-w-md w-full p-6")
        
        # Header del modal
        modal_header = Div(css_class="flex justify-between items-center mb-4")
        modal_header.add_component(H3("Nueva Lista Privada", css_class="text-lg font-semibold"))
        modal_header.add_component(Button("×", css_class="text-gray-400 hover:text-gray-600", onclick="cerrarModal()"))
        modal_dialog.add_component(modal_header)
        
        # Formulario
        form = Form(action="/listas-privadas/crear", method="POST")
        
        # Nombre de la lista
        form_group = FormGroup("Nombre de la lista")
        form_group.add_component(Input(
            type="text",
            name="nombre",
            placeholder="Ej: Libros de fantasía",
            required=True,
            css_class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        ))
        form.add_component(form_group)
        
        # Descripción
        form_group = FormGroup("Descripción (opcional)")
        form_group.add_component(TextArea(
            name="descripcion",
            placeholder="Describe tu lista...",
            rows=3,
            css_class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        ))
        form.add_component(form_group)
        
        # Nivel de privacidad
        form_group = FormGroup("Nivel de privacidad")
        select = Select(name="nivel_privacidad", css_class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500")
        select.add_option("privada", "Privada (solo yo)")
        select.add_option("amigos", "Visible para amigos")
        select.add_option("compartida", "Compartida con usuarios específicos")
        form_group.add_component(select)
        form.add_component(form_group)
        
        # Botones
        button_group = Div(css_class="flex gap-3 mt-6")
        button_group.add_component(Button("Cancelar", 
                                        type="button",
                                        css_class="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-700 py-2 px-4 rounded",
                                        onclick="cerrarModal()"))
        button_group.add_component(Button("Crear Lista", 
                                        type="submit",
                                        css_class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded"))
        form.add_component(button_group)
        
        modal_dialog.add_component(form)
        modal_content.add_component(modal_dialog)
        modal.add_component(modal_content)
        
        return modal
    
    def _render_error(self, mensaje: str) -> str:
        """Renderizar página de error"""
        page = HTMLPage("Error")
        container = Div(css_class="container mx-auto px-4 py-8 text-center")
        container.add_component(H1("Error", css_class="text-2xl font-bold text-red-600 mb-4"))
        container.add_component(P(mensaje, css_class="text-gray-600"))
        page.add_component(container)
        return page.render()
