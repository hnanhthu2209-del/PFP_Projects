import os

_DATA_DIR = os.path.dirname(os.path.abspath(__file__))

USERS_FILE = os.path.join(_DATA_DIR, "users.txt")
COMPONENTS_FILE = os.path.join(_DATA_DIR, "components.txt")
ORDERS_FILE = os.path.join(_DATA_DIR, "orders.txt")


def _read_lines(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.rstrip("\n") for line in f if line.strip()]
    except FileNotFoundError:
        return None


# ── USERS ───────────────────────────────────────────────────────────────────

def load_users(user_cls):
    lines = _read_lines(USERS_FILE)
    if lines is None:
        return None
    users = []
    for line in lines:
        try:
            username, password, role = line.split("|")
            users.append(user_cls(username, password, role))
        except ValueError:
            print(f"[!] Skipping invalid line in users.txt: {line}")
    return users


def save_users(users):
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            for u in users:
                f.write(f"{u.username}|{u.password}|{u.role}\n")
        return True
    except OSError as e:
        print(f"[!] Could not save users.txt: {e}")
        return False


# ── COMPONENTS & PC MODEL SERIES (single file) ──────────────────────────────

def load_components(component_cls, series_cls):
    lines = _read_lines(COMPONENTS_FILE)
    if lines is None:
        return None, None

    series = []
    components = []
    section = None
    for line in lines:
        if line == "[SERIES]":
            section = "series"
            continue
        if line == "[COMPONENTS]":
            section = "components"
            continue

        try:
            parts = line.split("|")
            if section == "series":
                series_id, brand, name, category = parts
                series.append(series_cls(int(series_id), brand, name, category))
            elif section == "components":
                cid, name, category, price, stock, description, compat = parts
                compatible_with = [int(x) for x in compat.split(",") if x.strip()]
                components.append(component_cls(
                    int(cid), name, category, int(float(price)), int(stock),
                    description, compatible_with
                ))
        except ValueError:
            print(f"[!] Skipping invalid line in components.txt: {line}")
    return components, series


def save_components(components, series):
    try:
        with open(COMPONENTS_FILE, "w", encoding="utf-8") as f:
            f.write("[SERIES]\n")
            for s in series:
                f.write(f"{s.series_id}|{s.brand}|{s.name}|{s.category}\n")
            f.write("[COMPONENTS]\n")
            for c in components:
                compat = ",".join(str(sid) for sid in c.compatible_with)
                f.write(f"{c.component_id}|{c.name}|{c.category}|{c.price}|{c.stock}|{c.description}|{compat}\n")
        return True
    except OSError as e:
        print(f"[!] Could not save components.txt: {e}")
        return False


# ── ORDERS ──────────────────────────────────────────────────────────────────

def load_orders(order_cls):
    lines = _read_lines(ORDERS_FILE)
    if lines is None:
        return None

    orders = []
    max_id = 0
    for line in lines:
        try:
            order_id, buyer_username, items_text, total_price = line.split("|")
            items = []
            for item_text in items_text.split(";"):
                component_id, component_name, quantity, subtotal = item_text.split(":")
                items.append((int(component_id), component_name, int(quantity), int(float(subtotal))))
            order = order_cls(buyer_username, items)
            order.order_id = int(order_id)
        except ValueError:
            print(f"[!] Skipping invalid line in orders.txt: {line}")
            continue
        max_id = max(max_id, order.order_id)
        orders.append(order)

    order_cls._next_id = max_id + 1
    return orders


def save_orders(orders):
    try:
        with open(ORDERS_FILE, "w", encoding="utf-8") as f:
            for o in orders:
                items_text = ";".join(
                    f"{component_id}:{component_name}:{quantity}:{subtotal}"
                    for component_id, component_name, quantity, subtotal in o.items
                )
                f.write(f"{o.order_id}|{o.buyer_username}|{items_text}|{o.total_price}\n")
        return True
    except OSError as e:
        print(f"[!] Could not save orders.txt: {e}")
        return False
