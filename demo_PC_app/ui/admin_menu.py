import data.store as store
from models.component import Component
from models.order import Order


# ── COMPONENTS MANAGEMENT ──────────────────────────────────────────────────────

def components_mgmt():
    while True:
        print("\n" + "=" * 50)
        print("  COMPONENTS MANAGEMENT")
        print("=" * 50)
        print("  1. Show All Components")
        print("  2. Add Component")
        print("  3. Search Components")
        print("  4. Back")
        print("-" * 50)
        choice = input("Select option: ").strip()

        if choice == "1":
            _show_all_components()
        elif choice == "2":
            _add_component()
        elif choice == "3":
            _search_components()
        elif choice == "4":
            return
        else:
            print("[!] Invalid option.")


def _show_all_components():
    print("\n--- ALL COMPONENTS ---")
    if not store.components:
        print("No components available.")
    else:
        for c in store.components:
            print(" ", c)


def _add_component():
    print("\n--- ADD COMPONENT ---")
    try:
        name = input("Name: ").strip()
        category = input("Category (CPU/GPU/RAM/Storage/Motherboard/PSU/Other): ").strip()
        price = float(input("Price ($): ").strip())
        stock = int(input("Stock quantity: ").strip())
        cid = store.get_next_component_id()
        component = Component(cid, name, category, price, stock)
        store.components.append(component)
        print(f"[✓] Component added: {component}")
    except ValueError:
        print("[!] Invalid input. Component not added.")


def _search_components():
    print("\n--- SEARCH COMPONENTS ---")
    keyword = input("Enter keyword (name or category): ").strip().lower()
    results = [c for c in store.components
               if keyword in c.name.lower() or keyword in c.category.lower()]
    if not results:
        print("No components found.")
    else:
        print(f"\nFound {len(results)} result(s):")
        for c in results:
            print(" ", c)


# ── ORDERS MANAGEMENT ─────────────────────────────────────────────────────────

def orders_mgmt():
    while True:
        print("\n" + "=" * 50)
        print("  ORDERS MANAGEMENT")
        print("=" * 50)
        print("  1. Show All Orders")
        print("  2. Add Order (manual)")
        print("  3. Search Orders")
        print("  4. Back")
        print("-" * 50)
        choice = input("Select option: ").strip()

        if choice == "1":
            _show_all_orders()
        elif choice == "2":
            _add_order()
        elif choice == "3":
            _search_orders()
        elif choice == "4":
            return
        else:
            print("[!] Invalid option.")


def _show_all_orders():
    print("\n--- ALL ORDERS ---")
    if not store.orders:
        print("No orders yet.")
    else:
        for o in store.orders:
            print(" ", o)


def _add_order():
    print("\n--- ADD ORDER (MANUAL) ---")
    try:
        buyer = input("Buyer username: ").strip()
        _show_all_components()
        cid = int(input("Component ID: ").strip())
        component = store.find_component_by_id(cid)
        if component is None:
            print("[!] Component not found.")
            return
        qty = int(input(f"Quantity (available: {component.stock}): ").strip())
        if qty <= 0 or qty > component.stock:
            print("[!] Invalid quantity.")
            return
        total = qty * component.price
        order = Order(buyer, component.component_id, component.name, qty, total)
        store.orders.append(order)
        component.stock -= qty
        print(f"[✓] Order added: {order}")
    except ValueError:
        print("[!] Invalid input.")


def _search_orders():
    print("\n--- SEARCH ORDERS ---")
    keyword = input("Enter buyer username or component name: ").strip().lower()
    results = [o for o in store.orders
               if keyword in o.buyer_username.lower() or keyword in o.component_name.lower()]
    if not results:
        print("No orders found.")
    else:
        print(f"\nFound {len(results)} result(s):")
        for o in results:
            print(" ", o)


# ── ADMIN MAIN MENU ───────────────────────────────────────────────────────────

def admin_menu(user):
    while True:
        print("\n" + "=" * 50)
        print(f"  ADMIN MENU  |  Logged in as: {user.username}")
        print("=" * 50)
        print("  1. Components Management")
        print("  2. Orders Management")
        print("  3. Log Out")
        print("-" * 50)
        choice = input("Select option: ").strip()

        if choice == "1":
            components_mgmt()
        elif choice == "2":
            orders_mgmt()
        elif choice == "3":
            print("\n[✓] Logged out.")
            return
        else:
            print("[!] Invalid option.")
