import os
from dotenv import load_dotenv
from supabase import create_client
from BookWorms.utils.security import hash_password


class DBBroker:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        load_dotenv(dotenv_path)

        self.supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

    def create_user(self, email: str, username: str, password: str):
        password_hash = hash_password(password)

        result = self.supabase.table("usuarios").insert({
            "email": email,
            "user": username,
            "passw": password_hash,
            "amigos": [],
            "es_admin": False
        }).execute()

        return result.data[0]

    def get_user_by_username(self, username: str):
        result = self.supabase.table("usuarios").select("*").eq("user", username).execute()

        return result.data

    def get_user_by_id(self, user_id):
        """Obtiene un usuario por su ID.
        
        Args:
            user_id: ID del usuario (puede ser int o str)
            
        Returns:
            Dict con la información del usuario o None si no se encuentra
        """
        try:
            # Convertir a entero si es posible
            user_id = int(user_id)

            result = self.supabase.table("usuarios")\
                .select("*")\
                .eq("id", user_id)\
                .maybe_single()\
                .execute()
                
            if not result.data:
                print(f"No se encontró el usuario con ID: {user_id}")
                return None
                
            return result.data
            
        except Exception as e:
            print(f"Error al buscar usuario con ID {user_id}: {e}")
            return None

    def buscar_libros(self, texto: str):
        # Armar patrón ILIKE
        pattern = f"%{texto}%"
        # print("🔍 dbbroker.buscar_libros – patrón:", pattern)

        result = (
            self.supabase
            .table("libros")
            .select("*")
            .ilike("titulo", pattern)
            .execute()
        )
        # print("🔎 dbbroker.buscar_libros – resultado:", result.data)
        return result.data or []

    def buscar_usuarios(self, username: str):
        pattern = f"%{username.lower()}%"
        # print("🔍 Buscando usuarios con patrón:", pattern)
        result = self.supabase.table("usuarios") \
            .select("*") \
            .ilike("user", pattern) \
            .execute()
        # print("🔎 Resultado raw de Supabase:", result.data)
        return result.data or []

    def agregar_amigo(self, user_id: int, amigo_id: int):
        result = self.supabase.table("usuarios").select("amigos").eq("id", user_id).single().execute()
        amigos = result.data["amigos"]

        amigos_int = list(map(int, amigos)) if amigos else []

        if amigo_id not in amigos_int:
            amigos_int.append(amigo_id)

        amigos_str = list(map(str, amigos_int))

        self.supabase.table("usuarios").update({
            "amigos": amigos_str}).eq("id", user_id).execute()

    def eliminar_amigo(self, user_id: int, amigo_id: int):
        result = self.supabase.table("usuarios").select("amigos").eq("id", user_id).single().execute()
        amigos = result.data["amigos"]

        amigos_int = list(map(int, amigos)) if amigos else []

        if amigo_id in amigos_int:
            amigos_int.remove(amigo_id)

        amigos_str = list(map(str, amigos_int))

        self.supabase.table("usuarios").update({
            "amigos": amigos_str}).eq("id", user_id).execute()

    def get_amigos_from_user_id(self, user_id: str) -> list:
        """"
        Dado un ID de usuario, devuelve los nombres de usuario de sus amigos.
        """
        result = self.supabase.table("usuarios").select("amigos").eq("id", user_id).single().execute()
        amigos = result.data["amigos"]

        amigos_int = list(map(int, amigos)) if amigos else []
        lista_amigos = []

        for i in amigos_int:
            amigo = self.get_user_by_id(i)["user"]
            lista_amigos.append(amigo)

        return lista_amigos

    def insert_current_user(self, current_user: str):
        result = self.supabase.table("current_user").insert({
            "current_user": current_user
        }).execute()

        return result.data

    def get_last_current_user(self):
        result = self.supabase.table("current_user") \
            .select("current_user") \
            .order("id", desc=True) \
            .limit(1) \
            .execute()

        return result.data[0]["current_user"] if result.data else None

    def alta_libro(self, titulo, isbn, autor, editorial, sinopsis):
        self.supabase.table("libros").insert({
            "titulo": titulo,
            "isbn": int(isbn),
            "autor": autor,
            "editorial": editorial,
            "sinopsis": sinopsis
        }).execute()

    def baja_libro(self, isbn):
        self.supabase.table("libros").delete().eq("isbn", int(isbn)).execute()

    def es_admin(self, username):
        result = self.supabase.table("usuarios").select("*").eq("user", username).execute()
        result = result.data[0]["es_admin"]

        if result:
            return True
        else:
            return False

    def handle_like(self, post_id):
        last_username = self.supabase.table("current_user") \
            .select("current_user") \
            .order("id", desc=True) \
            .limit(1) \
            .execute().data[0]["current_user"]
        user_id = self.supabase.table("usuarios").select("*").eq("user", last_username).execute().data[0]['id']

        likes = self.supabase.table("publicaciones").select("*").eq("id", post_id).single().execute().data["likes"]
        likes_int = list(map(int, likes)) if likes else []

        if user_id in likes_int:
            likes_int.remove(user_id)
        else:
            likes_int.append(user_id)

        likes_str = list(map(str, likes_int))

        self.supabase.table("publicaciones").update({
            "likes": likes_str}).eq("id", post_id).execute()

    def insert_comment(self, commenter_id: int, publicacion_id: int, comentario: str):
        response = self.supabase.table("comentarios").insert({
            "commenter_id": commenter_id,
            "publicacion_id": publicacion_id,
            "comentario": comentario
        }).execute()
        return response.data

    def delete_comment(self, comment_id: int):
        response = self.supabase.table("comentarios").delete().eq("id", comment_id).execute()
        return response.data

    def get_comments_by_post(self, publicacion_id) -> list[dict]:
        """Obtiene los comentarios de una publicación con información del autor.
        
        Args:
            publicacion_id: ID de la publicación (puede ser int o str)
            
        Returns:
            Lista de diccionarios con la información de los comentarios y sus autores
        """
        try:
            # Convertir a entero si es posible, si no, devolver lista vacía
            try:
                publicacion_id = int(publicacion_id)
            except (ValueError, TypeError):
                print(f"ID de publicación inválido: {publicacion_id}")
                return []
                
            print(f"Buscando comentarios para publicación ID: {publicacion_id} (tipo: {type(publicacion_id)})")
            
            # Primero obtenemos los comentarios de la publicación
            try:
                response = self.supabase.table("comentarios")\
                    .select("*")\
                    .eq("publicacion_id", publicacion_id)\
                    .order("id", desc=False)\
                    .execute()
                
                if not response.data:
                    print(f"No se encontraron comentarios para la publicación {publicacion_id}")
                    return []

            except Exception as query_error:
                print(f"Error en la consulta de comentarios: {query_error}")
                return []
                
            # Procesamos los comentarios para incluir el nombre de usuario
            comments = []
            for comment in response.data:
                try:
                    # Obtener información del usuario por separado
                    commenter_id = comment.get('commenter_id')
                    author_username = 'Usuario desconocido'
                    
                    if commenter_id is not None:
                        try:
                            user_data = self.get_user_by_id(commenter_id)
                            if user_data and 'user' in user_data:  # Nota: en get_user_by_id el campo es 'user' no 'username'
                                author_username = user_data['user']
                        except Exception as user_error:
                            print(f"Error al cargar usuario {commenter_id}: {user_error}")
                    
                    comments.append({
                        'id': comment.get('id'),
                        'commenter_id': commenter_id,
                        'publicacion_id': comment.get('publicacion_id'),
                        'comentario': comment.get('comentario', ''),
                        'created_at': comment.get('created_at'),
                        'author': author_username
                    })
                except Exception as e:
                    print(f"Error procesando comentario {comment.get('id')}: {e}")
                    comments.append({
                        'id': comment.get('id'),
                        'commenter_id': comment.get('commenter_id'),
                        'publicacion_id': comment.get('publicacion_id'),
                        'comentario': comment.get('comentario', ''),
                        'created_at': comment.get('created_at'),
                        'author': 'Usuario desconocido'
                    })
                    continue
                    
            return comments
            
        except Exception as e:
            print(f"Error al obtener comentarios para la publicación {publicacion_id}: {e}")
            return []

    def get_user_es_admin_by_id(self, user_id: int):
        result = self.supabase.table("usuarios").select("es_admin").eq("id", user_id).execute()

        return result.data[0].get("es_admin", False) if result.data else None

    # Crea una lista privada para un usuario
    def create_private_list(self, user_id: int, title: str) -> None:
        self.supabase.table("listas_privadas").insert({
            "user_id": user_id,
            "titulo": title
        }).execute()

    # Crea las tres listas por defecto
    """def create_default_private_lists(self, user_id: int) -> None:
        for title in ["Libros Leídos", "Libros Leyendo", "Libros por Leer"]:
            self.create_private_list(user_id, title)"""

    def create_default_private_lists(self, user_id: int) -> None:
        titles = ["Libros Leídos", "Libros Leyendo", "Libros por Leer"]
        for title in titles:
            try:
                res = (
                    self.supabase
                    .table("listas_privadas")
                    .insert({"user_id": user_id, "titulo": title})
                    .execute()
                )
                # print(f"Crear lista “{title}” para {user_id} → filas: {len(res.data or [])}, data: {res.data}")
            except Exception as e:
                raise RuntimeError(f"Error creando lista “{title}”: {e}")

    # PARA DEBUG
    def get_private_lists(self, user_id: int) -> list[dict]:
        """Devuelve todas las listas privadas de un usuario."""
        try:
            result = (
                self.supabase
                .table("listas_privadas")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )
            # print(f"DEBUG private lists for {user_id} →", result.data)
            return result.data or []

        except Exception as e:
            # print(f"Error al obtener listas privadas para {user_id}: {e}")
            return []

    def insert_current_user_es_admin(self, current_user: str, es_admin: bool):
        result = self.supabase.table("current_user").update({"es_admin": es_admin}).eq("current_user", current_user).execute()

        return result.data

    def reporte_general(self, report_name: str) -> list[dict]:
        res = (
            self.supabase
            .rpc("reporte_general", {"report_name": report_name})
            .execute()
        )
        return res.data or []

    def reporte_libros_mas_leidos(self) -> list[dict]:
        """Llama al RPC SQL reporte_libros_mas_leidos."""
        # res = self.supabase.rpc("reporte_libros_mas_leidos").execute()
        res = self.supabase.rpc("reporte_libros_mas_leidos", {}).execute()
        return res.data or []

    def reporte_libros_por_leer(self) -> list[dict]:
        """Llama al RPC SQL reporte_libros_por_leer."""
        # res = self.supabase.rpc("reporte_libros_por_leer").execute()
        res = self.supabase.rpc("reporte_libros_por_leer", {}).execute()
        return res.data or []

    def reporte_usuarios_seguidos(self) -> list[dict]:
        """Llama al RPC SQL reporte_usuarios_mas_seguidos."""
        # res = self.supabase.rpc("reporte_usuarios_mas_seguidos").execute()
        res = self.supabase.rpc("reporte_usuarios_mas_seguidos", {}).execute()
        return res.data or []
