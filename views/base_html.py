"""
Clases Python para construir HTML dinámicamente
Implementa el patrón Builder para construcción de elementos HTML
Evita el uso de templates estáticos
"""
from typing import List, Dict, Optional, Union

class HTMLElement:
    """Clase base para todos los elementos HTML"""
    
    def __init__(self, tag: str, content: str = "", **attributes):
        self.tag = tag
        self.content = content
        self.attributes = attributes
        self.children: List['HTMLElement'] = []
    
    def add_attribute(self, name: str, value: str):
        """Añade un atributo al elemento"""
        self.attributes[name] = value
        return self
    
    def add_child(self, child: Union['HTMLElement', str]):
        """Añade un elemento hijo"""
        self.children.append(child)
        return self
    
    def add_children(self, children: List[Union['HTMLElement', str]]):
        """Añade múltiples elementos hijos"""
        self.children.extend(children)
        return self
    
    def render_attributes(self) -> str:
        """Renderiza los atributos del elemento"""
        if not self.attributes:
            return ""
        
        attrs = []
        for key, value in self.attributes.items():
            # Convertir class_name a class
            if key == "class_name":
                key = "class"
            attrs.append(f'{key}="{value}"')
        
        return " " + " ".join(attrs)
    
    def render(self) -> str:
        """Renderiza el elemento HTML completo"""
        attrs = self.render_attributes()
        
        # Elementos auto-cerrados
        if self.tag in ['img', 'input', 'br', 'hr', 'meta', 'link']:
            return f"<{self.tag}{attrs} />"
        
        # Renderizar contenido y hijos
        content_parts = []
        if self.content:
            content_parts.append(self.content)
        
        for child in self.children:
            if isinstance(child, HTMLElement):
                content_parts.append(child.render())
            else:
                content_parts.append(str(child))
        
        content = "".join(content_parts)
        
        return f"<{self.tag}{attrs}>{content}</{self.tag}>"

class HTMLPage:
    """Clase para construir una página HTML completa"""
    
    def __init__(self, title: str = "Bookworms"):
        self.title = title
        self.head_elements: List[HTMLElement] = []
        self.body_elements: List[HTMLElement] = []
        self._setup_default_head()
    
    def _setup_default_head(self):
        """Configura elementos por defecto del head"""
        self.head_elements.extend([
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Title(self.title),
            self._get_default_styles()
        ])
    
    def _get_default_styles(self) -> HTMLElement:
        """Retorna los estilos CSS por defecto"""
        css = """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8fafc;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .navbar {
            background-color: #2563eb;
            color: white;
            padding: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .navbar-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }
        
        .navbar-brand {
            font-size: 1.5rem;
            font-weight: bold;
            text-decoration: none;
            color: white;
        }
        
        .navbar-nav {
            display: flex;
            list-style: none;
            gap: 1rem;
            flex-wrap: wrap;
        }
        
        .navbar-nav a {
            color: white;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            transition: background-color 0.2s;
        }
        
        .navbar-nav a:hover {
            background-color: rgba(255,255,255,0.1);
        }
        
        .search-container {
            display: flex;
            gap: 0.5rem;
        }
        
        .search-input {
            padding: 0.5rem;
            border: none;
            border-radius: 4px;
            min-width: 200px;
        }
        
        .search-btn {
            padding: 0.5rem 1rem;
            background-color: #1d4ed8;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        
        .main-content {
            padding: 2rem 0;
            min-height: calc(100vh - 200px);
        }
        
        .card {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .btn {
            display: inline-block;
            padding: 0.5rem 1rem;
            background-color: #2563eb;
            color: white;
            text-decoration: none;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        .btn:hover {
            background-color: #1d4ed8;
        }
        
        .btn-secondary {
            background-color: #6b7280;
        }
        
        .btn-secondary:hover {
            background-color: #4b5563;
        }
        
        .btn-danger {
            background-color: #dc2626;
        }
        
        .btn-danger:hover {
            background-color: #b91c1c;
        }
        
        .form-group {
            margin-bottom: 1rem;
        }
        
        .form-label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        .form-input {
            width: 100%;
            padding: 0.5rem;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            font-size: 1rem;
        }
        
        .form-input:focus {
            outline: none;
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }
        
        .alert {
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 1rem;
        }
        
        .alert-error {
            background-color: #fef2f2;
            color: #dc2626;
            border: 1px solid #fecaca;
        }
        
        .alert-success {
            background-color: #f0fdf4;
            color: #16a34a;
            border: 1px solid #bbf7d0;
        }
        
        .grid {
            display: grid;
            gap: 1rem;
        }
        
        .grid-2 {
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }
        
        .grid-3 {
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        }
        
        .text-center {
            text-align: center;
        }
        
        .text-muted {
            color: #6b7280;
        }
        
        .mb-1 { margin-bottom: 0.5rem; }
        .mb-2 { margin-bottom: 1rem; }
        .mb-3 { margin-bottom: 1.5rem; }
        .mt-1 { margin-top: 0.5rem; }
        .mt-2 { margin-top: 1rem; }
        .mt-3 { margin-top: 1.5rem; }
        
        @media (max-width: 768px) {
            .navbar-content {
                flex-direction: column;
                align-items: stretch;
            }
            
            .navbar-nav {
                justify-content: center;
            }
            
            .search-container {
                justify-content: center;
            }
            
            .search-input {
                min-width: auto;
                flex: 1;
            }
        }
        """
        
        return Style(css)
    
    def add_to_head(self, element: HTMLElement):
        """Añade un elemento al head"""
        self.head_elements.append(element)
        return self
    
    def add_to_body(self, element: HTMLElement):
        """Añade un elemento al body"""
        self.body_elements.append(element)
        return self
    
    def render(self) -> str:
        """Renderiza la página HTML completa"""
        head_content = "".join([elem.render() for elem in self.head_elements])
        body_content = "".join([elem.render() for elem in self.body_elements])
        
        return f"""<!DOCTYPE html>
<html lang="es">
<head>
{head_content}
</head>
<body>
{body_content}
</body>
</html>"""

# Elementos HTML específicos

class Title(HTMLElement):
    def __init__(self, content: str):
        super().__init__("title", content)

class Meta(HTMLElement):
    def __init__(self, **attributes):
        super().__init__("meta", **attributes)

class Style(HTMLElement):
    def __init__(self, css: str):
        super().__init__("style", css)

class Script(HTMLElement):
    def __init__(self, content: str = "", src: str = None):
        attributes = {}
        if src:
            attributes["src"] = src
        super().__init__("script", content, **attributes)

class Div(HTMLElement):
    def __init__(self, content: str = "", **attributes):
        super().__init__("div", content, **attributes)

class Span(HTMLElement):
    def __init__(self, content: str = "", **attributes):
        super().__init__("span", content, **attributes)

class H1(HTMLElement):
    def __init__(self, content: str = "", **attributes):
        super().__init__("h1", content, **attributes)

class H2(HTMLElement):
    def __init__(self, content: str = "", **attributes):
        super().__init__("h2", content, **attributes)

class H3(HTMLElement):
    def __init__(self, content: str = "", **attributes):
        super().__init__("h3", content, **attributes)

class P(HTMLElement):
    def __init__(self, content: str = "", **attributes):
        super().__init__("p", content, **attributes)

class A(HTMLElement):
    def __init__(self, content: str = "", href: str = "#", **attributes):
        super().__init__("a", content, href=href, **attributes)

class Button(HTMLElement):
    def __init__(self, content: str = "", button_type: str = "button", **attributes):
        super().__init__("button", content, type=button_type, **attributes)

class Input(HTMLElement):
    def __init__(self, input_type: str = "text", **attributes):
        super().__init__("input", type=input_type, **attributes)

class Textarea(HTMLElement):
    def __init__(self, content: str = "", **attributes):
        super().__init__("textarea", content, **attributes)

class Select(HTMLElement):
    def __init__(self, **attributes):
        super().__init__("select", **attributes)

class Option(HTMLElement):
    def __init__(self, content: str = "", value: str = "", **attributes):
        super().__init__("option", content, value=value, **attributes)

class Form(HTMLElement):
    def __init__(self, action: str = "", method: str = "POST", **attributes):
        super().__init__("form", action=action, method=method, **attributes)

class Label(HTMLElement):
    def __init__(self, content: str = "", for_attr: str = "", **attributes):
        if for_attr:
            attributes["for"] = for_attr
        super().__init__("label", content, **attributes)

class Ul(HTMLElement):
    def __init__(self, **attributes):
        super().__init__("ul", **attributes)

class Li(HTMLElement):
    def __init__(self, content: str = "", **attributes):
        super().__init__("li", content, **attributes)

class Img(HTMLElement):
    def __init__(self, src: str = "", alt: str = "", **attributes):
        super().__init__("img", src=src, alt=alt, **attributes)

class Nav(HTMLElement):
    def __init__(self, **attributes):
        super().__init__("nav", **attributes)

class Header(HTMLElement):
    def __init__(self, **attributes):
        super().__init__("header", **attributes)

class Main(HTMLElement):
    def __init__(self, **attributes):
        super().__init__("main", **attributes)

class Footer(HTMLElement):
    def __init__(self, **attributes):
        super().__init__("footer", **attributes)

class Section(HTMLElement):
    def __init__(self, **attributes):
        super().__init__("section", **attributes)

class Article(HTMLElement):
    def __init__(self, **attributes):
        super().__init__("article", **attributes)

# Componentes compuestos

class Navbar:
    """Componente navbar reutilizable"""
    
    @staticmethod
    def create(user_data: Dict = None) -> Nav:
        navbar = Nav(class_name="navbar")
        container = Div(class_name="container")
        navbar_content = Div(class_name="navbar-content")
        
        # Brand
        brand = A("📚 Bookworms", href="/", class_name="navbar-brand")
        navbar_content.add_child(brand)
        
        if user_data:
            # Navigation links
            nav_list = Ul(class_name="navbar-nav")
            nav_items = [
                ("Feed", "/feed"),
                ("Listas Públicas", "/listas-publicas"),
                ("Listas Privadas", "/listas-privadas"),
                ("Amigos", "/amigos"),
                ("Configuración", "/configuracion")
            ]
            
            for text, url in nav_items:
                li = Li()
                li.add_child(A(text, href=url))
                nav_list.add_child(li)
            
            navbar_content.add_child(nav_list)
            
            # Search form
            search_form = Form(action="/buscar", method="GET", class_name="search-container")
            search_input = Input(
                input_type="text", 
                name="q", 
                placeholder="Buscar libros o @usuarios...",
                class_name="search-input"
            )
            search_btn = Button("Buscar", button_type="submit", class_name="search-btn")
            
            search_form.add_children([search_input, search_btn])
            navbar_content.add_child(search_form)
            
            # User menu
            user_menu = Div(class_name="navbar-nav")
            user_menu.add_child(A(f"@{user_data.get('username', 'Usuario')}", href="/configuracion"))
            user_menu.add_child(A("Salir", href="/logout"))
            navbar_content.add_child(user_menu)
        
        container.add_child(navbar_content)
        navbar.add_child(container)
        
        return navbar

class Card:
    """Componente card reutilizable"""
    
    @staticmethod
    def create(title: str = "", content: str = "", class_name: str = "card") -> Div:
        card = Div(class_name=class_name)
        
        if title:
            card.add_child(H3(title, class_name="mb-2"))
        
        if content:
            card.add_child(P(content))
        
        return card

class FormGroup:
    """Componente form group reutilizable"""
    
    @staticmethod
    def create(label_text: str, input_name: str, input_type: str = "text", 
               placeholder: str = "", required: bool = False, value: str = "") -> Div:
        group = Div(class_name="form-group")
        
        # Label
        label = Label(label_text, for_attr=input_name, class_name="form-label")
        group.add_child(label)
        
        # Input
        input_attrs = {
            "name": input_name,
            "id": input_name,
            "class_name": "form-input"
        }
        
        if placeholder:
            input_attrs["placeholder"] = placeholder
        if required:
            input_attrs["required"] = "required"
        if value:
            input_attrs["value"] = value
        
        if input_type == "textarea":
            input_elem = Textarea(value, **input_attrs)
        else:
            input_elem = Input(input_type=input_type, **input_attrs)
        
        group.add_child(input_elem)
        
        return group

class Alert:
    """Componente alert reutilizable"""
    
    @staticmethod
    def create(message: str, alert_type: str = "info") -> Div:
        class_name = f"alert alert-{alert_type}"
        return Div(message, class_name=class_name)
