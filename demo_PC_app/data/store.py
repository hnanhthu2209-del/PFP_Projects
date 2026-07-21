from models.user import create_user
from models.component import Component
from models.order import Order
from models.pc_model_series import PCModelSeries
from data import file_manager

# All data lives in the .txt files under data/ (users.txt, components.txt,
# orders.txt) — nothing is hardcoded here. This module just loads them into
# memory at startup and exposes save_*() to write changes back to those files.
users = file_manager.load_users(create_user) or []

components, pc_model_series = file_manager.load_components(Component, PCModelSeries)
components = components or []
pc_model_series = pc_model_series or []

orders = file_manager.load_orders(Order) or []

_component_next_id = max((c.component_id for c in components), default=0) + 1


def save_users():
    return file_manager.save_users(users)


def save_components():
    return file_manager.save_components(components, pc_model_series)


def save_orders():
    return file_manager.save_orders(orders)


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


def component_matches(component, keyword):
    # Spaces are ignored on both sides, so a keyword like "rtx4090" still
    # matches a name like "NVIDIA RTX 4090".
    keyword = keyword.replace(" ", "")
    name = component.name.lower().replace(" ", "")
    category = component.category.lower().replace(" ", "")
    return keyword in name or keyword in category
