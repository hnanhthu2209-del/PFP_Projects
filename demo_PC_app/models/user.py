class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role  # "admin" or "buyer"


class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, "admin")


class Buyer(User):
    def __init__(self, username, password):
        super().__init__(username, password, "buyer")


def create_user(username, password, role):
    if role == "admin":
        return Admin(username, password)
    elif role == "buyer":
        return Buyer(username, password)
    return User(username, password, role)
