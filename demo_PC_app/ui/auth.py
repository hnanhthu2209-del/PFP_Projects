import data.store as store


def login():
    print("\n" + "=" * 50)
    print("       PC COMPONENTS SALES SYSTEM")
    print("=" * 50)
    while True:
        username = input("\nEnter username: ").strip()
        user = store.find_user(username)
        if user is None:
            print("[!] Username not found. Restarting login...")
            continue

        password = input("Enter password: ").strip()
        if password != user.password:
            print("[!] Wrong password. Please try again.")
            continue

        print(f"\n[✓] Login successful! Welcome, {user.username} ({user.role.upper()})")
        return user
