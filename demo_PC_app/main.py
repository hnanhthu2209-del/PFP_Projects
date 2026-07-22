from ui.auth import login
from ui.buyer_menu import buyer_menu
from ui.admin_menu import admin_menu


def main():
    while True:
        user = login()
        user.enter_menu(admin_menu, buyer_menu)

        again = input("\nReturn to login screen? (y/n): ").strip().lower()
        if again != "y":
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
