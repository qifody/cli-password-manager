
from storage import FileStorage
from manager import PasswordManager
from getpass import getpass

def run():
    storage = FileStorage("data/vault.json")
    pm = PasswordManager(storage)

    password = getpass("Password: ")

    while not pm.login(password):
        print("Wrong password")


        password = getpass("Password: ")

    while True:
        print(
            """
            1 Add entry
            2 Get entry
            3 Delete entry
            4 List entries
            5 Exit
            """
        )
        choice = input().strip()

        if choice == "1":
            site = input("Site: ")
            username = input("Username: ")
            password = getpass("Password: ")
            try:
                pm.add_entry(site, username, password)
                print("Added successfully")
            except ValueError as e:
                print("Entry already exists")


        elif choice == "2":
            site = input("Site: ")
            try:
                entry = pm.get_entry(site)
                print("Username:", entry["username"])
                print("Password:", entry["password"])
            except KeyError as e:
                print("Entry not found")

        elif choice == "3":
            site = input("Site: ")
            try:
                pm.delete_entry(site)
                print("Deleted successfully")
            except KeyError:
                print("Entry not found")


        elif choice == "4":
            entries = pm.list_entries()
            if len(entries) == 0:
                print("No entries found")
            else:
                for site in entries:
                    print(site)

        elif choice == "5":
            print("Exiting")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    run()

