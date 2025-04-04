from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password  # Store hashed passwords in real apps

    def get_id(self):
        return str(self.id)
