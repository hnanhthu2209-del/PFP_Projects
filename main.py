from models.user import Admin, Organizer, Student

USERS = [
    Admin("A001", "Alice", "admin123"), # this is the object we use
    Organizer("B001", "Bob", "org123"),
    Student("S001", "Charlie", "stu123"),
    Student("S002", "Diana", "dia123")
    ]
    
print("\n======== Campus Event System ==========")
print("           Welcome! Please log in")
print("==========================================")

def login():

    name = input("\nEnter your user name: ").strip()
    password = input("Enter your password: ").strip()

    """Check name and password valid"""
    for user in USERS:
        if user.name.lower() == name.lower() and user.password.lower() == password.lower():
            print(f"\nLogin successful! Welcome, {user.name } ({user.role.upper()})")
            return user

    print("\nInvalid name or password. Please try again.")
    return None

"""Display menu"""
def show_menu(user):
    options = user.get_menu()
    print(f"\n---- {user.role.upper()} MENU ----")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")

    while True: 
        choice = input("Enter number of your option you chose: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice)
        print(f"Please enter the number in list of options!")

'''Main loop'''
def main():
    
    while True: #run forever until manually break
        user = None

        while user is None: 
            user = login()

        # Show menu until logout
        while True:
            choice = show_menu(user)
            selected = user.get_menu()[choice - 1]

            if selected == "Logout":
                print(f"\nGoodbye, {user.name}!")
                break
            else:
                print(f"\n →  '{selected}' coming soon...")

if __name__ == "__main__":
    main()








