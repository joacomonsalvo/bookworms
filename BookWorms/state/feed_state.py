import reflex as rx
from BookWorms.state.auth_state import AuthState
from BookWorms.models.post_model import Post


class FeedState(rx.State):
    posts: list[dict] = []
    show_delete_confirm: bool = False
    post_to_delete: int | None = None

    def load_posts(self):
        self.posts = Post.get_all_posts()

    def show_delete_dialog(self, post_id: int):
        """Show delete confirmation dialog"""
        self.post_to_delete = post_id
        self.show_delete_confirm = True

    def confirm_delete_with_user_id(self, user_id: int):
        """Confirm and delete the post with user ID"""
        if self.post_to_delete is not None:
            success = Post.delete_post(self.post_to_delete, user_id)
            if success:
                self.load_posts()  # Reload posts after deletion
        self.show_delete_confirm = False
        self.post_to_delete = None

    def confirm_delete(self):
        """Confirm and delete the post"""
        if self.post_to_delete is not None:
            # Get the current user ID from AuthState
            current_user_id = AuthState.get_current_user_id()
            if current_user_id is not None:
                success = Post.delete_post(self.post_to_delete, current_user_id)
                if success:
                    self.load_posts()  # Reload posts after deletion
        self.show_delete_confirm = False
        self.post_to_delete = None

    def cancel_delete(self):
        """Cancel delete operation"""
        self.show_delete_confirm = False
        self.post_to_delete = None

    def like(self, post_id: int):
        Post.handle_like(post_id)
        self.load_posts()
