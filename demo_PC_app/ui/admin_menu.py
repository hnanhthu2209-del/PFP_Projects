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
        print("  3. Edit Component")
        print("  4. Delete Component")
        print("  5. Search Components")
        print("  6. Manage Compatible Products")
        print("  7. Back")
        print("-" * 50)
        choice = input("Select option: ").strip()

        if choice == "1":
            _show_all_components()
        elif choice == "2":
            _add_component()
        elif choice == "3":
            _edit_component()
        elif choice == "4":
            _delete_component()
        elif choice == "5":
            _search_components()
        elif choice == "6":
            _manage_compatible_products()
        elif choice == "7":
            return
        else:
            print("[!] Invalid option.")


def _show_all_components():
    print("\n--- ALL COMPONENTS ---")
    if not store.components:
        print("No components available.")
    else:
        for c in store.components:
            print(" ", c.detail_str(store.find_series_by_id))


def _add_component():
    print("\n--- ADD COMPONENT ---")
    try:
        name = input("Name: ").strip()
        category = input("Category (CPU/GPU/RAM/Storage/Motherboard/PSU/Other): ").strip()
        price = float(input("Price (VND): ").strip())
        while price < 1000 or price != int(price):
            print("[!] Please enter the valid input")
            return
        stock = int(input("Stock quantity: ").strip())
        cid = store.get_next_component_id()
        component = Component(cid, name, category, price, stock)
        store.components.append(component)
        if store.save_components():
            print(f"[✓] Component added: {component}")
        else:
            print(f"[!] Component added, but saving to file failed: {component}")
    except ValueError:
        print("[!] Invalid input. Component not added.")


def _edit_component():
    print("\n--- EDIT COMPONENT ---")
    _show_all_components()
    if not store.components:
        return
    try:
        cid = int(input("\nEnter Component ID to edit: ").strip())
    except ValueError:
        print("[!] Invalid ID.")
        return
    component = store.find_component_by_id(cid)
    if component is None:
        print("[!] Component not found.")
        return

    print(f"\nEditing: {component}")
    print("(Press Enter to keep the current value)")

    name = input(f"Name [{component.name}]: ").strip()
    if name:
        component.name = name

    category = input(f"Category [{component.category}]: ").strip()
    if category:
        component.category = category

    price_input = input(f"Price (VND) [{component.price}]: ").strip()
    if price_input:
        try:
            price = float(price_input)
        except ValueError:
            print("[!] Please enter the valid input")
            return
        if price < 1000 or price != int(price):
            print("[!] Please enter the valid input")
            return
        component.price = int(price)

    stock_input = input(f"Stock [{component.stock}]: ").strip()
    if stock_input:
        try:
            component.stock = int(stock_input)
        except ValueError:
            print("[!] Invalid input.")
            return

    description = input(f"Description [{component.description}]: ").strip()
    if description:
        component.description = description

    if store.save_components():
        print(f"[✓] Component updated: {component}")
    else:
        print(f"[!] Component updated, but saving to file failed: {component}")


def _delete_component():
    print("\n--- DELETE COMPONENT ---")
    _show_all_components()
    if not store.components:
        return
    try:
        cid = int(input("\nEnter Component ID to delete: ").strip())
    except ValueError:
        print("[!] Invalid ID.")
        return
    component = store.find_component_by_id(cid)
    if component is None:
        print("[!] Component not found.")
        return

    confirm = input(f"Type 'yes' to permanently delete '{component.name}': ").strip().lower()
    if confirm != "yes":
        print("[!] Cancelled.")
        return

    store.components.remove(component)
    if store.save_components():
        print(f"[✓] Component permanently deleted: {component.name}")
    else:
        print("[!] Deleted from memory, but saving to file failed.")


def _show_all_series():
    print("\n--- AVAILABLE PC MODEL SERIES ---")
    for s in store.pc_model_series:
        print(f"  {s}")


def _manage_compatible_products():
    print("\n--- MANAGE COMPATIBLE PC MODEL SERIES ---")
    _show_all_components()
    try:
        cid = int(input("\nEnter Component ID to edit: ").strip())
    except ValueError:
        print("[!] Invalid ID.")
        return
    component = store.find_component_by_id(cid)
    if component is None:
        print("[!] Component not found.")
        return

    print(f"\nEditing: {component}")
    if component.compatible_with:
        print("Current compatible PC series:")
        for sid in component.compatible_with:
            s = store.find_series_by_id(sid)
            print(f"  - {s}" if s else f"  - [Unknown ID {sid}]")
    else:
        print("No compatible PC series set yet.")

    print("\n  1. Add compatible PC series")
    print("  2. Remove a compatible PC series")
    print("  3. Clear all compatible PC series")
    print("  4. Cancel")
    sub = input("Select option: ").strip()

    if sub == "1":
        _show_all_series()
        raw = input("\nEnter Series ID(s) to add (comma-separated): ").strip()
        try:
            ids = [int(x.strip()) for x in raw.split(",") if x.strip()]
        except ValueError:
            print("[!] Invalid input — enter numbers only.")
            return
        added = []
        for sid in ids:
            s = store.find_series_by_id(sid)
            if s is None:
                print(f"  [!] Series ID {sid} not found, skipped.")
            elif sid in component.compatible_with:
                print(f"  [!] {s} already in the list, skipped.")
            else:
                component.compatible_with.append(sid)
                added.append(str(s))
        if added:
            if store.save_components():
                print(f"[✓] Added: {', '.join(added)}")
            else:
                print(f"[!] Added, but saving to file failed: {', '.join(added)}")

    elif sub == "2":
        if not component.compatible_with:
            print("[!] Nothing to remove.")
            return
        for i, sid in enumerate(component.compatible_with, 1):
            s = store.find_series_by_id(sid)
            print(f"  {i}. {s}" if s else f"  {i}. [Unknown ID {sid}]")
        try:
            idx = int(input("Enter number to remove: ").strip()) - 1
            if 0 <= idx < len(component.compatible_with):
                removed_id = component.compatible_with.pop(idx)
                s = store.find_series_by_id(removed_id)
                if store.save_components():
                    print(f"[✓] Removed: {s if s else removed_id}")
                else:
                    print(f"[!] Removed, but saving to file failed: {s if s else removed_id}")
            else:
                print("[!] Invalid selection.")
        except ValueError:
            print("[!] Invalid input.")

    elif sub == "3":
        component.compatible_with.clear()
        if store.save_components():
            print("[✓] All compatible PC series cleared.")
        else:
            print("[!] Cleared, but saving to file failed.")

    elif sub == "4":
        return
    else:
        print("[!] Invalid option.")


def _search_components():
    print("\n--- SEARCH COMPONENTS ---")
    keyword = input("Enter keyword (name or category): ").strip().lower()
    results = [c for c in store.components if store.component_matches(c, keyword)]
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
    buyer = input("Buyer username: ").strip()
    items = []

    while True:
        _show_all_components()
        try:
            cid = int(input("\nComponent ID (or 0 to finish adding items): ").strip())
        except ValueError:
            print("[!] Invalid input.")
            continue

        if cid == 0:
            break

        component = store.find_component_by_id(cid)
        if component is None:
            print("[!] Component not found.")
            continue

        already_added = sum(qty for item_cid, name, qty, sub in items if item_cid == component.component_id)
        available = component.stock - already_added

        try:
            qty = int(input(f"Quantity (available: {available}): ").strip())
        except ValueError:
            print("[!] Invalid input.")
            continue

        if qty <= 0 or qty > available:
            print("[!] Invalid quantity.")
            continue

        subtotal = qty * component.price
        items.append((component.component_id, component.name, qty, subtotal))
        print(f"[✓] Added to order: {component.name} x{qty}")

    if not items:
        print("[!] No items added. Order cancelled.")
        return

    for component_id, component_name, qty, subtotal in items:
        component = store.find_component_by_id(component_id)
        component.stock -= qty

    order = Order(buyer, items)
    store.orders.append(order)
    orders_saved = store.save_orders()
    components_saved = store.save_components()
    if orders_saved and components_saved:
        print(f"[✓] Order added:\n{order}")
        print("Warranty stock: 2 years start from now")
    else:
        print(f"[!] Order added, but saving to file failed:\n{order}")


def _search_orders():
    print("\n--- SEARCH ORDERS ---")
    keyword = input("Enter buyer username or component name: ").strip().lower()
    results = []
    for o in store.orders:
        if keyword in o.buyer_username.lower():
            results.append(o)
            continue
        for component_id, component_name, quantity, subtotal in o.items:
            if keyword in component_name.lower():
                results.append(o)
                break
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
