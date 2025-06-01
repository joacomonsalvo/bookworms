"""
Vista para el login con magic link
Implementa el patrón MVC - Vista
"""
from views.base_html import HTMLPage, Div, H1, H2, P, Form, Button, Alert, FormGroup

class LoginView:
    """Vista para manejo de login y autenticación"""
    
    def render_login_form(self, error: str = None) -> str:
        """Renderiza el formulario de login"""
        page = HTMLPage("Iniciar Sesión - Bookworms")
        
        # Container principal
        container = Div(class_name="container")
        main_content = Div(class_name="main-content")
        
        # Card de login
        login_card = Div(class_name="card", style="max-width: 400px; margin: 2rem auto;")
        
        # Título
        login_card.add_child(H1("📚 Bookworms", class_name="text-center mb-3"))
        login_card.add_child(H2("Iniciar Sesión", class_name="text-center mb-3"))
        
        # Mensaje de error si existe
        if error:
            login_card.add_child(Alert.create(error, "error"))
        
        # Descripción
        description = P(
            "Ingresa tu email y te enviaremos un enlace mágico para acceder a tu cuenta.",
            class_name="text-center text-muted mb-3"
        )
        login_card.add_child(description)
        
        # Formulario de login
        login_form = Form(action="/login", method="POST")
        
        # Campo email
        email_group = FormGroup.create(
            "Email", 
            "email", 
            "email", 
            "tu@email.com", 
            required=True
        )
        login_form.add_child(email_group)
        
        # Botón submit
        submit_btn = Button(
            "Enviar enlace mágico", 
            button_type="submit", 
            class_name="btn w-100 mb-3"
        )
        login_form.add_child(submit_btn)
        
        login_card.add_child(login_form)
        
        # Link a registro
        signup_link = P(class_name="text-center")
        signup_link.add_child("¿No tienes cuenta? ")
        signup_link.add_child(A("Regístrate aquí", href="/signup"))
        login_card.add_child(signup_link)
        
        main_content.add_child(login_card)
        container.add_child(main_content)
        page.add_to_body(container)
        
        return page.render()
    
    def render_magic_link_sent(self, email: str) -> str:
        """Renderiza la página de confirmación de envío de magic link"""
        page = HTMLPage("Enlace Enviado - Bookworms")
        
        container = Div(class_name="container")
        main_content = Div(class_name="main-content")
        
        # Card de confirmación
        confirmation_card = Div(class_name="card", style="max-width: 500px; margin: 2rem auto;")
        
        # Título
        confirmation_card.add_child(H1("📧 Enlace Enviado", class_name="text-center mb-3"))
        
        # Mensaje de éxito
        success_alert = Alert.create(
            f"Hemos enviado un enlace mágico a {email}. Revisa tu bandeja de entrada y haz clic en el enlace para acceder.",
            "success"
        )
        confirmation_card.add_child(success_alert)
        
        # Instrucciones
        instructions = Div(class_name="mb-3")
        instructions.add_child(P("📱 Revisa también tu carpeta de spam"))
        instructions.add_child(P("⏰ El enlace expira en 15 minutos"))
        instructions.add_child(P("🔄 Puedes solicitar un nuevo enlace si es necesario"))
        confirmation_card.add_child(instructions)
        
        # Botón para volver al login
        back_btn = A(
            "Volver al login", 
            href="/login", 
            class_name="btn btn-secondary w-100"
        )
        confirmation_card.add_child(back_btn)
        
        main_content.add_child(confirmation_card)
        container.add_child(main_content)
        page.add_to_body(container)
        
        return page.render()
