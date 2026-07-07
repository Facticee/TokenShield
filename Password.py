from rich.console import Console
import secrets
import string
import json
import os


console = Console()


DB_FILE = "vault.json"

def load_vault():
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f:
            return json.load(f)
    return {}

def save_vault(vault):
    with open(DB_FILE, "w") as f:
        json.dump(vault, f, indent=4)



def generate_random_password(pwlength=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return "".join(secrets.choice(chars) for _ in range(pwlength))

def main():
    console.print("[bold cyan]💎 Welcome - Password Vault[/bold cyan]")






    while True:
        print("\n1. See every Entry")
        print("2. Search Entry")
        print("3. Add Entry")
        print("4. Password Generator")
        print("5. Close")

        choice = input("Choice: ")

        if choice == "5":
            print("Programm closed.")
            break
        elif choice == "4":
            length = input("Length (Default 16): ")

            if length.isdigit():
                length = int(length)
            else:
                length = 16

        elif choice == "3":

            app = input("App/Website: ")
            username = input("Username: ")
            password = input("Password: ")
            notes = input("Notes: ")


            vault = load_vault()

            vault[app] = {
                "username": username,
                "password": password,
                "notes": notes
            }

            save_vault(vault)

            print(generate_random_password(length))
        else:
            print("Test")

if __name__ == "__main__":
    main()
