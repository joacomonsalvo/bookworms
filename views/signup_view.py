"""
Vista para el registro de nuevos usuarios
Implementa el patrón MVC - Vista
"""
from views.base_html import HTMLPage, Div, H1, H2, P, Form, Button, Alert, FormGroup, A

class SignupView:
    """Vista para manejo de registro de usuarios"""
    
    def render_signup_form(self, error: str = None) -> str:
        """Renderiza el formulario de registro"""
        page = HTMLPage("Registro - Bookworms")
        
        container = Div(class_name="container")
        main_content = Div(class_name="main-content")
        
        # Card de registro
        signup_card = Div(class_name="card", style="max-width: 500px; margin: 2rem auto;")
        
        # Título
        signup_card.add_child(H1("📚 Bookworms", class_name="text-center mb-3"))
        signup_card.add_child(H2("Crear Cuenta", class_name="text-center mb-3"))
        
        # Mensaje de error si existe
        if error:
            signup_card.add_child(Alert.create(error, "error"))
        
        # Descripción
        description = P(
            "Únete a nuestra comunidad de amantes de los libros y comienza a compartir tus lecturas favoritas.",
            class_name="text-center text-muted mb-3"
        )
        signup_card.add_child(description)
        
        # Formulario de registro
        signup_form = Form(action="/signup", method="POST")
        
        # Campo nombre completo
        fullname_group = FormGroup.create(
            "Nombre Completo", 
            "full_name", 
            "text", 
            "Tu nombre completo", 
            required=True
        )
        signup_form.add_child(fullname_group)
        
        # Campo username
        username_group = FormGroup.create(
            "Nombre de Usuario", 
            "username", 
            "text", 
            "usuario123", 
            required=True
        )
        signup_form.add_child(username_group)
        
        # Campo email
        email_group = FormGroup.create(
            "Email", 
            "email", 
            "email", 
            "tu@email.com", 
            required=True
        )
        signup_form.add_child(email_group)
        
        # Botón submit
        submit_btn = Button(
            "Crear Cuenta", 
            button_type="submit", 
            class_name="btn w-100 mb-3"
        )
        signup_form.add_child(submit_btn)
        
        signup_card.add_child(signup_form)
        
        # Link a login
        login_link = P(class_name="text-center")
        login_link.add_child("¿Ya tienes cuenta? ")
        login_link.add_child(A("Inicia sesión aquí", href="/login"))
        signup_card.add_child(login_link)
        
        main_content.add_child(signup_card)
        container.add_child(main_content)
        page.add_to_body(container)
        
        return page.render()
    
    def render_signup_success(self) -> str:
        """Renderiza la página de éxito del registro"""
        page = HTMLPage("Registro Exitoso - Bookworms")
        
        container = Div(class_name="container")
        main_content = Div(class_name="main-content")
        
        # Card de éxito
        success_card = Div(class_name="card", style="max-width: 500px; margin: 2rem auto;")
        
        # Título
        success_card.add_child(H1("🎉 ¡Bienvenido!", class_name="text-center mb-3"))
        
        # Mensaje de éxito
        success_alert = Alert.create(
            "Tu cuenta ha sido creada exitosamente. Hemos enviado un email de bienvenida con más información.",
            "success"
        )
        success_card.add_child(success_alert)
        
        # Instrucciones
        instructions = Div(class_name="mb-3")
        instructions.add_child(H3("¿Qué sigue?", class_name="mb-2"))
        instructions.add_child(P("✅ Revisa tu email para confirmar tu cuenta"))
        instructions.add_child(P("📚 Explora nuestra biblioteca de libros"))
        instructions.add_child(P("👥 Conecta con otros lectores"))
        instructions.add_child(P("📝 Comparte tus reseñas y listas"))
        success_card.add_child(instructions)
        
        # Botón para ir al login
        login_btn = A(
            "Iniciar Sesión", 
            href="/login", 
            class_name="btn w-100"
        )
        success_card.add_child(login_btn)
        
        main_content.add_child(success_card)
        container.add_child(main_content)
        page.add_to_body(container)
        
        return page.render()
