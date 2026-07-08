import data.store as store
from models.order import Order


def view_orders(buyer_username):
    print("\n--- MY PURCHASED ORDERS ---")
    my_orders = [o for o in store.orders if o.buyer_username == buyer_username]
    if not my_orders:
        print("No orders found.")
    else:
        for o in my_orders:
            print(" ", o)


_current_buyer = ""


def buyer_menu(user):
    global _current_buyer
    _current_buyer = user.username

    while True:
        print("\n" + "=" * 50)
        print(f"  BUYER MENU  |  Logged in as: {user.username}")
        print("=" * 50)
        print("  1. Search Components")
        print("  2. View My Orders")
        print("  3. Log Out")
        print("-" * 50)
        choice = input("Select option: ").strip()

        if choice == "1":
            _search_and_buy(user.username)
        elif choice == "2":
            view_orders(user.username)
        elif choice == "3":
            print("\n[✓] Logged out.")
            return
        else:
            print("[!] Invalid option.")


def _search_and_buy(buyer_username):
    print("\n--- SEARCH COMPONENTS ---")
    keyword = input("Enter keyword (name or category): ").strip().lower()
    results = [c for c in store.components
               if keyword in c.name.lower() or keyword in c.category.lower()]
    if not results:
        print("No components found.")
        return

    print(f"\nFound {len(results)} result(s):")
    for c in results:
        print(" ", c)

    detail = input("\nEnter component ID to view details & compatible PC series (or press Enter to skip): ").strip()
    if detail:
        try:
            dcid = int(detail)
            dc = store.find_component_by_id(dcid)
            if dc is None:
                print("[!] Component not found.")
            else:
                print("\n" + "=" * 50)
                print(dc.detail_str(store.find_series_by_id))
                print("=" * 50)
        except ValueError:
            print("[!] Invalid input.")

    buy = input("\nEnter component ID to purchase (or press Enter to skip): ").strip()
    if not buy:
        return
    try:
        cid = int(buy)
        component = store.find_component_by_id(cid)
        if component is None:
            print("[!] Component not found.")
        elif component.stock <= 0:
            print("[!] Out of stock.")
        else:
            qty = int(input(f"Enter quantity (available: {component.stock}): ").strip())
            if qty <= 0 or qty > component.stock:
                print("[!] Invalid quantity.")
            else:
                total = qty * component.price
                order = Order(buyer_username, component.component_id,
                              component.name, qty, total)
                store.orders.append(order)
                component.stock -= qty
                store.save_orders()
                store.save_components()
                print(f"[✓] Order placed! {order}")
    except ValueError:
        print("[!] Invalid input.")
