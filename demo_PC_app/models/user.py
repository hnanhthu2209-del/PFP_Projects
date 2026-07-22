class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role  # "admin" or "buyer"

    def get_menu_route(self):
        raise NotImplementedError

    def enter_menu(self, admin_menu_func, buyer_menu_func):
        raise NotImplementedError


class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, "admin")

    def get_menu_route(self):
        return "admin_menu"

    def enter_menu(self, admin_menu_func, buyer_menu_func):
        admin_menu_func(self)


class Buyer(User):
    def __init__(self, username, password):
        super().__init__(username, password, "buyer")

    def get_menu_route(self):
        return "buyer_menu"

    def enter_menu(self, admin_menu_func, buyer_menu_func):
        buyer_menu_func(self)


def create_user(username, password, role):
    if role == "admin":
        return Admin(username, password)
    elif role == "buyer":
        return Buyer(username, password)
    return User(username, password, role)
