"""
Vista para listas públicas de libros
Implementa el patrón MVC - Vista
"""
from views.base_html import HTMLPage, Div, H1, H2, H3, P, Form, Button, Input, Navbar, Card, A, Span
from models.auth import AuthService

class ListasPublicasView:
    """Vista para manejo de listas públicas"""
    
    def __init__(self):
        self.auth_service = AuthService()
    
    def render_listas_publicas(self, user_id: int, page: int = 1) -> str:
        """Renderiza la vista de listas públicas"""
        page_html = HTMLPage("Listas Públicas - Bookworms")
        
        # Obtener datos del usuario
        user_data = self.auth_service.get_user_by_id(user_id)
        
        # Navbar
        navbar = Navbar.create(user_data)
        page_html.add_to_body(navbar)
        
        # Container principal
        container = Div(class_name="container")
        main_content = Div(class_name="main-content")
        
        # Título y botón crear
        header = Div(style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;")
        header.add_child(H1("📋 Listas Públicas"))
        
        create_btn = A(
            "➕ Crear Lista Pública", 
            href="#", 
            class_name="btn",
            onclick="document.getElementById('create-modal').style.display='block'"
        )
        header.add_child(create_btn)
        main_content.add_child(header)
        
        # Filtros
        filters = self._render_filters()
        main_content.add_child(filters)
        
        # Grid de listas
        listas = self._get_public_lists(page)
        
        if listas:
            grid = Div(class_name="grid grid-3")
            for lista in listas:
                lista_card = self._render_lista_card(lista, user_id)
                grid.add_child(lista_card)
            main_content.add_child(grid)
            
            # Paginación
            pagination = self._render_pagination(page)
            main_content.add_child(pagination)
        else:
            no_lists = Card.create(
                "No hay listas públicas", 
                "Aún no hay listas públicas disponibles. ¡Sé el primero en crear una!"
            )
            main_content.add_child(no_lists)
        
        # Modal para crear lista
        create_modal = self._render_create_modal()
        main_content.add_child(create_modal)
        
        container.add_child(main_content)
        page_html.add_to_body(container)
        
        return page_html.render()
    
    def _render_filters(self) -> Div:
        """Renderiza los filtros de búsqueda"""
        filters = Div(class_name="card mb-3")
        filters.add_child(H3("🔍 Filtros", class_name="mb-2"))
        
        filter_form = Form(action="/listas-publicas", method="GET")
        filter_grid = Div(class_name="grid grid-3")
        
        # Filtro por categoría
        category_group = Div(class_name="form-group")
        category_label = Label("Categoría", class_name="form-label")
        category_select = Select(name="categoria", class_name="form-input")
        
        categories = [
            ("", "Todas las categorías"),
            ("ficcion", "Ficción"),
            ("no-ficcion", "No ficción"),
            ("ciencia", "Ciencia"),
            ("historia", "Historia"),
            ("biografia", "Biografía"),
            ("fantasia", "Fantasía"),
            ("romance", "Romance"),
            ("misterio", "Misterio")
        ]
        
        for value, text in categories:
            option = Option(text, value=value)
            category_select.add_child(option)
        
        category_group.add_children([category_label, category_select])
        filter_grid.add_child(category_group)
        
        # Filtro por popularidad
        sort_group = Div(class_name="form-group")
        sort_label = Label("Ordenar por", class_name="form-label")
        sort_select = Select(name="orden", class_name="form-input")
        
        sort_options = [
            ("recientes", "Más recientes"),
            ("populares", "Más populares"),
            ("alfabetico", "Alfabético"),
            ("mas_libros", "Más libros")
        ]
        
        for value, text in sort_options:
            option = Option(text, value=value)
            sort_select.add_child(option)
        
        sort_group.add_children([sort_label, sort_select])
        filter_grid.add_child(sort_group)
        
        # Botón filtrar
        filter_btn = Button(
            "Aplicar Filtros", 
            button_type="submit", 
            class_name="btn"
        )
        filter_grid.add_child(filter_btn)
        
        filter_form.add_child(filter_grid)
        filters.add_child(filter_form)
        
        return filters
    
    def _render_lista_card(self, lista: dict, user_id: int) -> Div:
        """Renderiza una tarjeta de lista pública"""
        card = Div(class_name="card")
        
        # Header de la lista
        header = Div(class_name="mb-2")
        title_link = A(
            lista.get('nombre', 'Lista sin nombre'), 
            href=f"/lista/{lista.get('id')}",
            class_name="h3"
        )
        header.add_child(title_link)
        
        # Info del creador
        creator_info = Div(class_name="text-muted mb-2")
        creator_link = A(
            f"@{lista.get('creator_username', 'usuario')}", 
            href=f"/usuario/{lista.get('user_id')}"
        )
        creator_info.add_child("Creada por ")
        creator_info.add_child(creator_link)
        creator_info.add_child(f" • {self._format_time(lista.get('created_at'))}")
        header.add_child(creator_info)
        
        card.add_child(header)
        
        # Descripción
        if lista.get('descripcion'):
            description = P(lista.get('descripcion'), class_name="mb-2")
            card.add_child(description)
        
        # Estadísticas
        stats = Div(class_name="mb-2")
        book_count = lista.get('book_count', 0)
        follower_count = lista.get('follower_count', 0)
        
        stats.add_child(Span(f"📚 {book_count} libros", class_name="me-3"))
        stats.add_child(Span(f"👥 {follower_count} seguidores"))
        card.add_child(stats)
        
        # Acciones
        actions = Div(class_name="mt-2")
        
        # Botón seguir/no seguir
        is_following = lista.get('is_following', False)
        follow_form = Form(action="/lista/seguir", method="POST", style="display: inline;")
        follow_form.add_child(Input(type="hidden", name="lista_id", value=str(lista.get('id'))))
        
        follow_btn_text = "✅ Siguiendo" if is_following else "➕ Seguir"
        follow_btn_class = "btn btn-secondary" if is_following else "btn"
        
        follow_btn = Button(
            follow_btn_text, 
            button_type="submit", 
            class_name=follow_btn_class
        )
        follow_form.add_child(follow_btn)
        actions.add_child(follow_form)
        
        # Botón ver detalles
        view_btn = A(
            "👁️ Ver Lista", 
            href=f"/lista/{lista.get('id')}", 
            class_name="btn btn-secondary ml-2"
        )
        actions.add_child(view_btn)
        
        card.add_child(actions)
        
        return card
    
    def _render_create_modal(self) -> Div:
        """Renderiza el modal para crear nueva lista"""
        modal = Div(
            id="create-modal",
            style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000;"
        )
        
        modal_content = Div(
            class_name="card",
            style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); max-width: 500px; width: 90%;"
        )
        
        # Header del modal
        modal_header = Div(style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;")
        modal_header.add_child(H3("➕ Crear Lista Pública"))
        
        close_btn = Button(
            "✕", 
            class_name="btn btn-secondary",
            onclick="document.getElementById('create-modal').style.display='none'"
        )
        modal_header.add_child(close_btn)
        modal_content.add_child(modal_header)
        
        # Formulario
        create_form = Form(action="/lista/crear", method="POST")
        create_form.add_child(Input(type="hidden", name="es_publica", value="on"))
        
        # Nombre de la lista
        name_group = FormGroup.create(
            "Nombre de la Lista", 
            "nombre", 
            "text", 
            "Mi lista de libros favoritos", 
            required=True
        )
        create_form.add_child(name_group)
        
        # Descripción
        desc_group = FormGroup.create(
            "Descripción", 
            "descripcion", 
            "textarea", 
            "Describe de qué trata tu lista..."
        )
        create_form.add_child(desc_group)
        
        # Botones
        button_group = Div(style="display: flex; gap: 1rem; justify-content: flex-end;")
        
        cancel_btn = Button(
            "Cancelar", 
            class_name="btn btn-secondary",
            onclick="document.getElementById('create-modal').style.display='none'"
        )
        
        submit_btn = Button(
            "Crear Lista", 
            button_type="submit", 
            class_name="btn"
        )
        
        button_group.add_children([cancel_btn, submit_btn])
        create_form.add_child(button_group)
        
        modal_content.add_child(create_form)
        modal.add_child(modal_content)
        
        return modal
    
    def _render_pagination(self, current_page: int) -> Div:
        """Renderiza la paginación"""
        pagination = Div(class_name="pagination text-center mt-3")
        
        if current_page > 1:
            prev_link = A(
                "← Anterior", 
                href=f"/listas-publicas?page={current_page - 1}",
                class_name="btn btn-secondary"
            )
            pagination.add_child(prev_link)
        
        page_info = Span(f" Página {current_page} ", class_name="mx-2")
        pagination.add_child(page_info)
        
        next_link = A(
            "Siguiente →", 
            href=f"/listas-publicas?page={current_page + 1}",
            class_name="btn btn-secondary"
        )
        pagination.add_child(next_link)
        
        return pagination
    
    def _get_public_lists(self, page: int) -> list:
        """Obtiene las listas públicas"""
        try:
            from models.db_broker import DatabaseBroker
            db = DatabaseBroker()
            return db.get_public_lists(page)
        except Exception:
            return []
    
    def _format_time(self, timestamp: str) -> str:
        """Formatea el timestamp para mostrar"""
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            now = datetime.now(dt.tzinfo)
            diff = now - dt
            
            if diff.days > 0:
                return f"hace {diff.days} días"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"hace {hours} horas"
            else:
                return "hace un momento"
        except Exception:
            return "hace un momento"
    
    def crear_lista(self, data: dict) -> dict:
        """Crea una nueva lista pública"""
        try:
            from models.db_broker import DatabaseBroker
            db = DatabaseBroker()
            
            lista_id = db.create_public_list(data)
            if lista_id:
                return {'success': True, 'lista_id': lista_id}
            else:
                return {'success': False, 'error': 'Error al crear la lista'}
        except Exception as e:
            return {'success': False, 'error': f'Error: {str(e)}'}
