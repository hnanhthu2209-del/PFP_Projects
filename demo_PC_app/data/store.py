from models.user import User
from models.component import Component
from models.order import Order
from models.pc_model_series import PCModelSeries
from data import file_manager

# Seed data — only used the very first time the app runs, before the
# .txt data files exist. Once the files are created, they are the source
# of truth and this seed data is not read again.
_seed_users = [
    User("admin", "admin123", "admin"),
    User("buyer1", "pass123", "buyer"),
    User("buyer2", "pass456", "buyer"),
]

_seed_components = [
    Component(1, "Intel Core i9-14900K", "CPU",         589.99,  10, compatible_with=[2, 6, 8, 10, 12]),
    Component(2, "AMD Ryzen 9 7950X",    "CPU",         699.99,   8, compatible_with=[4, 6, 8, 10]),
    Component(3, "NVIDIA RTX 4090",      "GPU",        1599.99,   5, compatible_with=[2, 3, 6, 8, 9, 10]),
    Component(4, "AMD RX 7900 XTX",      "GPU",         999.99,   7, compatible_with=[3, 4, 6, 8, 9, 10]),
    Component(5, "Samsung 32GB DDR5 RAM","RAM",         129.99,  20, compatible_with=[1, 2, 3, 4, 6, 7, 8, 9, 10]),
    Component(6, "Samsung 990 Pro 2TB SSD","Storage",  179.99,  15, compatible_with=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]),
    Component(7, "ASUS ROG Maximus Z790","Motherboard", 599.99,   6, compatible_with=[2, 6, 8, 10]),
    Component(8, "Corsair HX1000i PSU",  "PSU",         249.99,  12, compatible_with=[2, 6, 8, 10, 12]),
]

_seed_pc_model_series = [
    PCModelSeries(1,  "Dell",       "XPS 15",               "Laptop"),
    PCModelSeries(2,  "Dell",       "XPS Tower",            "Desktop"),
    PCModelSeries(3,  "ASUS",       "ROG Strix G16",        "Laptop"),
    PCModelSeries(4,  "ASUS",       "ProArt Station PD5",   "Desktop"),
    PCModelSeries(5,  "HP",         "Spectre x360",         "Laptop"),
    PCModelSeries(6,  "HP",         "Omen 45L",             "Desktop"),
    PCModelSeries(7,  "Lenovo",     "ThinkPad X1 Carbon",   "Laptop"),
    PCModelSeries(8,  "Lenovo",     "Legion Tower 7i",      "Desktop"),
    PCModelSeries(9,  "MSI",        "Titan GT77 HX",        "Laptop"),
    PCModelSeries(10, "MSI",        "MEG Infinite X2",      "Desktop"),
    PCModelSeries(11, "Apple",      "MacBook Pro 16\"",     "Laptop"),
    PCModelSeries(12, "Microsoft",  "Surface Studio 2+",    "Desktop"),
]

_seed_orders = []

# Load persisted data from the .txt files in data/. If a file doesn't exist
# yet (first run), fall back to the seed data above and write it out so the
# file exists from then on.
users = file_manager.load_users(User)
if users is None:
    users = _seed_users
    file_manager.save_users(users)

components, pc_model_series = file_manager.load_components(Component, PCModelSeries)
if components is None:
    components = _seed_components
    pc_model_series = _seed_pc_model_series
    file_manager.save_components(components, pc_model_series)

orders = file_manager.load_orders(Order)
if orders is None:
    orders = _seed_orders
    file_manager.save_orders(orders)

_component_next_id = max((c.component_id for c in components), default=0) + 1


def save_users():
    file_manager.save_users(users)


def save_components():
    file_manager.save_components(components, pc_model_series)


def save_orders():
    file_manager.save_orders(orders)


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


def find_series_by_id(series_id):
    for s in pc_model_series:
        if s.series_id == series_id:
            return s
    return None
