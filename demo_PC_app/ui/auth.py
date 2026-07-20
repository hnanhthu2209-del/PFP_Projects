import data.store as store
from models.user import User


def login():
    print("\n" + "=" * 50)
    print("       PC COMPONENTS SALES SYSTEM")
    print("=" * 50)

    role = _choose_role()

    first_time = input("\nFirst time log in? (yes/no): ").strip().lower()
    if first_time in ("yes", "y"):
        _register(role)

    while True:
        username = input("\nEnter username: ").strip()
        user = store.find_user(username)
        if user is None or user.role != role:
            print("[!] Username not found for this role. Restarting login...")
            continue

        password = input("Enter password: ").strip()
        if password != user.password:
            print("[!] Wrong password. Please try again.")
            continue

        print(f"\n[✓] Login successful! Welcome, {user.username} ({user.role.upper()})")
        return user


def _choose_role():
    while True:
        role = input("\nAre you Admin or Buyer? (admin/buyer): ").strip().lower()
        if role in ("admin", "buyer"):
            return role
        print("[!] Please enter 'admin' or 'buyer'.")


def _register(role):
    print("\n--- CREATE NEW ACCOUNT ---")
    while True:
        username = input("Choose a username: ").strip()
        if store.find_user(username) is not None:
            print("[!] That username is already taken. Try another.")
            continue
        break

    password = input("Choose a password: ").strip()
    new_user = User(username, password, role)
    store.users.append(new_user)
    if store.save_users():
        print(f"[✓] Registration successful! You can now log in as {username}.")
    else:
        print("[!] Registered, but saving to file failed.")
