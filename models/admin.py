from usuario import Usuario


class Admin(Usuario):
    def __init__(self, ID, username, email, amigos, user_type):
        super().__init__(ID, username, email, amigos, user_type)
        self.user_type = user_type
