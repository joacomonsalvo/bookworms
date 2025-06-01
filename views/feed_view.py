"""
Vista para el feed principal de publicaciones
Implementa el patrón MVC - Vista
"""
from views.base_html import HTMLPage, Div, H1, H2, H3, P, Form, Button, Textarea, Navbar, Card, A, Span
from models.auth import AuthService

class FeedView:
    """Vista para el feed principal de publicaciones"""
    
    def __init__(self):
        self.auth_service = AuthService()
    
    def render_feed(self, user_id: int, page: int = 1) -> str:
        """Renderiza el feed principal"""
        page_html = HTMLPage("Feed - Bookworms")
        
        # Obtener datos del usuario
        user_data = self.auth_service.get_user_by_id(user_id)
        
        # Navbar
        navbar = Navbar.create(user_data)
        page_html.add_to_body(navbar)
        
        # Container principal
        container = Div(class_name="container")
        main_content = Div(class_name="main-content")
        
        # Título
        main_content.add_child(H1("📰 Feed de Publicaciones", class_name="mb-3"))
        
        # Grid layout
        grid = Div(class_name="grid grid-2")
        
        # Columna izquierda - Crear publicación
        left_column = Div()
        create_post_card = self._render_create_post_form()
        left_column.add_child(create_post_card)
        
        # Columna derecha - Publicaciones
        right_column = Div()
        posts = self._get_feed_posts(user_id, page)
        
        if posts:
            for post in posts:
                post_card = self._render_post_card(post, user_id)
                right_column.add_child(post_card)
        else:
            no_posts = Card.create(
                "No hay publicaciones", 
                "¡Sé el primero en compartir algo! Crea una publicación o sigue a otros usuarios para ver contenido."
            )
            right_column.add_child(no_posts)
        
        # Paginación
        pagination = self._render_pagination(page)
        right_column.add_child(pagination)
        
        grid.add_children([left_column, right_column])
        main_content.add_child(grid)
        container.add_child(main_content)
        page_html.add_to_body(container)
        
        return page_html.render()
    
    def _render_create_post_form(self) -> Div:
        """Renderiza el formulario para crear publicaciones"""
        card = Div(class_name="card")
        card.add_child(H3("✍️ Crear Publicación", class_name="mb-2"))
        
        form = Form(action="/publicacion/crear", method="POST")
        
        # Textarea para contenido
        content_group = Div(class_name="form-group")
        content_label = Label("¿Qué estás leyendo?", class_name="form-label")
        content_textarea = Textarea(
            placeholder="Comparte tus pensamientos sobre un libro, una reseña, o cualquier cosa relacionada con la lectura...",
            name="contenido",
            class_name="form-input",
            rows="4",
            required="required"
        )
        content_group.add_children([content_label, content_textarea])
        form.add_child(content_group)
        
        # Selector de tipo de publicación
        type_group = Div(class_name="form-group")
        type_label = Label("Tipo de publicación", class_name="form-label")
        type_select = Select(name="tipo", class_name="form-input")
        
        type_options = [
            ("general", "General"),
            ("reseña", "Reseña"),
            ("recomendacion", "Recomendación"),
            ("progreso", "Progreso de lectura")
        ]
        
        for value, text in type_options:
            option = Option(text, value=value)
            type_select.add_child(option)
        
        type_group.add_children([type_label, type_select])
        form.add_child(type_group)
        
        # Botón submit
        submit_btn = Button(
            "Publicar", 
            button_type="submit", 
            class_name="btn w-100"
        )
        form.add_child(submit_btn)
        
        card.add_child(form)
        return card
    
    def _render_post_card(self, post: dict, current_user_id: int) -> Div:
        """Renderiza una tarjeta de publicación"""
        card = Div(class_name="card")
        
        # Header del post
        post_header = Div(class_name="mb-2")
        
        # Info del usuario
        user_info = Div(style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;")
        user_link = A(
            f"@{post.get('username', 'usuario')}", 
            href=f"/usuario/{post.get('user_id')}"
        )
        post_time = Span(
            self._format_time(post.get('created_at')), 
            class_name="text-muted"
        )
        user_info.add_children([user_link, " • ", post_time])
        post_header.add_child(user_info)
        
        # Tipo de publicación
        if post.get('tipo') != 'general':
            type_badge = Span(
                f"📖 {post.get('tipo', '').title()}", 
                class_name="badge"
            )
            post_header.add_child(type_badge)
        
        card.add_child(post_header)
        
        # Contenido del post
        content = P(post.get('contenido', ''), class_name="mb-2")
        card.add_child(content)
        
        # Libro asociado si existe
        if post.get('libro_titulo'):
            book_info = Div(class_name="book-reference mb-2")
            book_info.add_child(P(f"📚 Sobre: {post.get('libro_titulo')}", class_name="text-muted"))
            card.add_child(book_info)
        
        # Acciones del post
        actions = self._render_post_actions(post, current_user_id)
        card.add_child(actions)
        
        return card
    
    def _render_post_actions(self, post: dict, current_user_id: int) -> Div:
        """Renderiza las acciones de una publicación (like, comentar, etc.)"""
        actions = Div(class_name="post-actions", style="display: flex; gap: 1rem; align-items: center;")
        
        # Botón de like
        like_form = Form(action="/like/toggle", method="POST", style="display: inline;")
        like_form.add_child(Input(type="hidden", name="publicacion_id", value=str(post.get('id'))))
        
        like_count = post.get('likes_count', 0)
        is_liked = post.get('is_liked_by_user', False)
        like_text = f"{'❤️' if is_liked else '🤍'} {like_count}"
        
        like_btn = Button(
            like_text, 
            button_type="submit", 
            class_name="btn-link",
            style="background: none; border: none; color: #2563eb; cursor: pointer;"
        )
        like_form.add_child(like_btn)
        actions.add_child(like_form)
        
        # Enlace a comentarios
        comment_count = post.get('comments_count', 0)
        comment_link = A(
            f"💬 {comment_count} comentarios", 
            href=f"/publicacion/{post.get('id')}"
        )
        actions.add_child(comment_link)
        
        # Botón compartir
        share_btn = Button(
            "🔗 Compartir", 
            class_name="btn-link",
            style="background: none; border: none; color: #2563eb; cursor: pointer;",
            onclick=f"navigator.share({{title: 'Publicación en Bookworms', url: window.location.origin + '/publicacion/{post.get('id')}'}})"
        )
        actions.add_child(share_btn)
        
        return actions
    
    def _render_pagination(self, current_page: int) -> Div:
        """Renderiza la paginación"""
        pagination = Div(class_name="pagination text-center mt-3")
        
        # Página anterior
        if current_page > 1:
            prev_link = A(
                "← Anterior", 
                href=f"/feed?page={current_page - 1}",
                class_name="btn btn-secondary"
            )
            pagination.add_child(prev_link)
        
        # Número de página actual
        page_info = Span(f" Página {current_page} ", class_name="mx-2")
        pagination.add_child(page_info)
        
        # Página siguiente
        next_link = A(
            "Siguiente →", 
            href=f"/feed?page={current_page + 1}",
            class_name="btn btn-secondary"
        )
        pagination.add_child(next_link)
        
        return pagination
    
    def _get_feed_posts(self, user_id: int, page: int) -> list:
        """Obtiene las publicaciones para el feed"""
        try:
            from models.db_broker import DatabaseBroker
            db = DatabaseBroker()
            return db.get_feed_posts(user_id, page)
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
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"hace {minutes} minutos"
            else:
                return "hace un momento"
        except Exception:
            return "hace un momento"
