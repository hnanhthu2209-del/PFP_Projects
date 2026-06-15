from models.user import User
from models.component import Component
from models.order import Order

# Seed users
users = [
    User("admin", "admin123", "admin"),
    User("buyer1", "pass123", "buyer"),
    User("buyer2", "pass456", "buyer"),
]

# Seed components
components = [
    Component(1, "Intel Core i9-14900K", "CPU", 589.99, 10),
    Component(2, "AMD Ryzen 9 7950X", "CPU", 699.99, 8),
    Component(3, "NVIDIA RTX 4090", "GPU", 1599.99, 5),
    Component(4, "AMD RX 7900 XTX", "GPU", 999.99, 7),
    Component(5, "Samsung 32GB DDR5 RAM", "RAM", 129.99, 20),
    Component(6, "Samsung 990 Pro 2TB SSD", "Storage", 179.99, 15),
    Component(7, "ASUS ROG Maximus Z790", "Motherboard", 599.99, 6),
    Component(8, "Corsair HX1000i PSU", "PSU", 249.99, 12),
]

# Orders list
orders = []

_component_next_id = 9

def get_next_component_id():
    global _component_next_id
    cid = _component_next_id
    _component_next_id += 1
    return cid

def find_user(username):
    for u in users:
        if u.username == username:
            return u
    return None

def find_component_by_id(component_id):
    for c in components:
        if c.component_id == component_id:
            return c
    return None
