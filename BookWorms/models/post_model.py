from BookWorms.models.user_model import User
from datetime import datetime


class Post:
    @staticmethod
    def get_all_posts():
        response = User.supabase_client().table("publicaciones").select("*").order("fecha", desc=True).execute()
        if hasattr(response, "data") and response.data:
            posts = []
            for p in response.data:
                # Get the username for the author
                user = User.get_user_by_id(p["author"])
                username = user["user"] if user else f"User {p['author']}"
                
                posts.append({
                    "id": p["id"],
                    "fecha": datetime.strptime(p["fecha"], "%Y-%m-%dT%H:%M:%S").strftime("%d/%m/%Y %H:%M"),
                    "titulo": p["titulo"],
                    "texto": p["text"],
                    "author": username,
                })
            return posts
        return []

    @staticmethod
    def delete_post(post_id: int, user_id: int | None) -> bool:
        """Delete a post if the user is the author"""
        if user_id is None:
            return False
            
        # First check if the post exists and belongs to the user
        response = User.supabase_client().table("publicaciones").select("*").eq("id", post_id).eq("author", user_id).execute()
        
        if not response.data:
            return False  # Post doesn't exist or user is not the author
        
        # Delete the post
        delete_response = User.supabase_client().table("publicaciones").delete().eq("id", post_id).execute()
        return True

    @staticmethod
    def create_post(title: str, text: str, author_id: int) -> bool:
        """Insert a new post into the publicaciones table."""
        from datetime import datetime
        now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        post_data = {
            "titulo": title,
            "text": text,
            "author": author_id,
            "fecha": now
        }
        # Defensive: Remove 'id' if present
        post_data.pop("id", None)
        response = User.supabase_client().table("publicaciones").insert(post_data).execute()
        return hasattr(response, "data") and bool(response.data)
