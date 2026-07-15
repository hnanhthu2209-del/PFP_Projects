import data.store as store
from currency import format_vnd


def view_orders(buyer_username):
    print("\n--- MY PURCHASED ORDERS ---")
    my_orders = [o for o in store.orders if o.buyer_username == buyer_username]
    if not my_orders:
        print("No orders found.")
    else:
        for o in my_orders:
            print(" ", o)


def buyer_menu(user):
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
            _search_components()
        elif choice == "2":
            view_orders(user.username)
        elif choice == "3":
            print("\n[✓] Logged out.")
            return
        else:
            print("[!] Invalid option.")


def _search_components():
    print("\n--- SEARCH COMPONENTS ---")
    keyword = input("Enter keyword (name or category): ").strip().lower()
    results = [c for c in store.components if store.component_matches(c, keyword)]
    if not results:
        print("No components found.")
        return

    print(f"\nFound {len(results)} result(s):")
    for c in results:
        print(f"  [{c.component_id}] {c.name} | Category: {c.category} | Price: {format_vnd(c.price)}")
        if c.compatible_with:
            print("    Compatible PC series:")
            for sid in c.compatible_with:
                s = store.find_series_by_id(sid)
                print(f"      - {s if s else f'[Unknown ID {sid}]'}")
        else:
            print("    Compatible PC series: none listed")
