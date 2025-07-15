import reflex as rx
from typing import List, Dict, Optional
from BookWorms.models.dbbroker import DBBroker
from BookWorms.state.auth_state import AuthState

class CommentsState(rx.State):
    # Estado para el comentario que se está escribiendo
    comment_text: str = ""
    
    # Lista de comentarios de la publicación actual
    comments: List[Dict] = []
    
    # Publicación actual
    post: Optional[Dict] = None
    
    # Estado de carga
    is_loading: bool = False
    
    # Renombramos post_id a current_post_id_value para evitar conflictos con el parámetro de ruta
    current_post_id_value: int = 0
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializar el ID de la publicación en el constructor
        self.current_post_id_value = 0
    
    def get_post_id_from_url(self) -> int:
        """Obtiene el ID de la publicación de la URL actual"""
        try:
            # Obtener el ID de los parámetros de la ruta
            if hasattr(self.router, 'params') and 'post_id' in self.router.params:
                post_id = self.router.params['post_id']
                if post_id and str(post_id).isdigit():
                    return int(post_id)
                    
            # Fallback: intentar extraer de la URL si no está en los parámetros
            if hasattr(self.router, 'url'):
                url = self.router.url
                if '/comments/' in url:
                    post_id_part = url.split('/comments/')[-1].split('/')[0].split('?')[0]
                    if post_id_part.isdigit():
                        return int(post_id_part)
                        
            print(f"No se pudo extraer el ID de la URL. Router: {vars(self.router)}")
            
        except Exception as e:
            print(f"Error al extraer el ID de la URL: {e}")
            
        return 0
    
    @rx.var
    def current_post_id(self) -> int:
        """Propiedad computada que devuelve el ID de la publicación actual"""
        return self.current_post_id_value
    
    async def load_comments(self):
        """Carga los comentarios de la publicación actual"""
        self.is_loading = True
        yield
        
        try:
            # Obtener el ID de la URL primero
            post_id = self.get_post_id_from_url()
            if not post_id:
                print("No se pudo obtener un ID de publicación válido de la URL")
                self.is_loading = False
                return
                
            # Actualizar el ID de la publicación actual
            self.current_post_id_value = post_id
            
            db = DBBroker()
            
            # Cargar la publicación
            try:
                post_result = db.supabase.table("publicaciones").select("*").eq("id", post_id).execute()
                
                if post_result.data:
                    post_data = post_result.data[0]
                    # Verificar si user_id es válido antes de intentar obtener el autor
                    user_id = post_data.get("user_id")
                    author_username = "Usuario desconocido"
                    
                    if user_id is not None and str(user_id).isdigit():
                        try:
                            author_data = db.get_user_by_id(int(user_id))
                            if author_data and 'user' in author_data:
                                author_username = author_data['user']
                        except Exception as e:
                            print(f"Error al cargar el autor: {e}")
                    
                    self.post = {
                        **post_data,
                        "author_username": author_username
                    }
                else:
                    print(f"No se encontró la publicación con ID: {post_id}")
                    self.post = None
                    
            except Exception as e:
                print(f"Error al cargar la publicación: {e}")
                self.post = None
                
            # Cargar comentarios
            try:
                comments = db.get_comments_by_post(self.current_post_id)
                self.comments = comments
            except Exception as e:
                print(f"Error al cargar comentarios: {e}")
                self.comments = []
                
        except Exception as e:
            print(f"Error en load_comments: {e}")
            self.comments = []
        finally:
            self.is_loading = False
        
        try:
            db = DBBroker()
            
            # Obtener la publicación
            post_result = db.supabase.table("publicaciones").select("*").eq("id", self.current_post_id).execute()
            
            if post_result.data:
                post_data = post_result.data[0]
                # Obtener el autor de la publicación
                author_data = db.get_user_by_id(post_data.get("user_id"))
                post_with_author = {
                    **post_data,
                    "author": author_data["user"] if author_data else "Usuario desconocido"
                }
                self.post = post_with_author
            
            # Obtener comentarios
            comments = db.get_comments_by_post(self.current_post_id)
            
            # Obtener los nombres de usuario de los autores de los comentarios
            for comment in comments:
                author_data = db.get_user_by_id(comment["commenter_id"])
                comment["author"] = author_data["user"] if author_data else "Usuario desconocido"
            
            self.comments = comments
            
        except Exception as e:
            print(f"Error al cargar comentarios: {str(e)}")
            self.comments = []
        finally:
            self.is_loading = False
    
    async def add_comment(self):
        """Agrega un nuevo comentario"""
        if not self.comment_text.strip() or not self.current_post_id:
            return
            
        self.is_loading = True
        yield
        
        try:
            # Obtener el estado de autenticación
            auth_state = await self.get_state(AuthState)
            if not auth_state.is_logged_in or not auth_state.current_user_id:
                print("Usuario no autenticado")
                self.is_loading = False
                return
            
            # Verificar que los IDs sean válidos
            if not auth_state.current_user_id or not self.current_post_id:
                print("Error: ID de usuario o publicación inválido")
                return
                
            try:
                # Insertar el comentario
                db = DBBroker()
                db.insert_comment(
                    commenter_id=int(auth_state.current_user_id),
                    publicacion_id=int(self.current_post_id),
                    comentario=self.comment_text.strip()
                )
                
                # Limpiar el campo de texto
                self.comment_text = ""
                
                # Recargar los comentarios
                self.comments = []  # Clear comments to show loading state
                # Since load_comments is a generator, we need to iterate through it
                async for _ in self.load_comments():
                    pass
                
            except Exception as db_error:
                print(f"Error al insertar el comentario: {db_error}")
                import traceback
                traceback.print_exc()
                return
            
        except Exception as e:
            print(f"Error al agregar comentario: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_loading = False
    
    async def delete_comment(self, comment_id: int):
        """Elimina un comentario"""
        if not comment_id:
            return
            
        self.is_loading = True
        yield
        
        try:
            # Verificar que el usuario esté autenticado
            auth_state = await self.get_state(AuthState)
            if not auth_state.is_logged_in or not auth_state.current_user_id:
                print("Usuario no autenticado")
                self.is_loading = False
                return
            
            # Verificar que el comentario pertenezca al usuario
            db = DBBroker()
            comment = next((c for c in self.comments if c.get('id') == comment_id), None)
            
            if not comment:
                print("Comentario no encontrado")
                self.is_loading = False
                return
                
            if str(comment.get('commenter_id')) != str(auth_state.current_user_id):
                print("No tienes permiso para eliminar este comentario")
                self.is_loading = False
                return
            
            # Eliminar el comentario
            db.delete_comment(comment_id)
            
            # Recargar los comentarios
            self.comments = []  # Clear comments to show loading state
            # Since load_comments is a generator, we need to iterate through it
            async for _ in self.load_comments():
                pass
            
        except Exception as e:
            print(f"Error al eliminar comentario: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_loading = False
            
    def set_comment_text(self, text: str):
        """Actualiza el texto del comentario que se está escribiendo"""
        self.comment_text = text
