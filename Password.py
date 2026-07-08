import json
import os
import base64
import secrets
import string
import getpass  # Ermöglicht die komplett verdeckte Passworteingabe im Terminal
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from rich.console import Console
from rich.table import Table

console = Console()
DB_FILE = "vault.json"

def get_encryption_key(master_password: str, salt: bytes) -> bytes:

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

def generate_random_password(length: int = 16) -> str:

    characters = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return "".join(secrets.choice(characters) for _ in range(length))


def load_vault(master_password: str) -> dict:

    if not os.path.exists(DB_FILE):
        new_salt = os.urandom(16)
        return {"salt": base64.b64encode(new_salt).decode(), "entries": {}}

    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)

        salt = base64.b64decode(data["salt"])
        key = get_encryption_key(master_password, salt)
        fernet = Fernet(key)

        decrypted_data = fernet.decrypt(data["encrypted_data"].encode()).decode()
        return {"salt": data["salt"], "entries": json.loads(decrypted_data)}
    except Exception:
        console.print("\n[bold red]❌ Wrong password![/bold red]\n")
        return None

def save_vault(master_password: str, vault: dict):

    salt = base64.b64decode(vault["salt"])
    key = get_encryption_key(master_password, salt)
    fernet = Fernet(key)

    json_data = json.dumps(vault["entries"]).encode()
    encrypted_data = fernet.encrypt(json_data).decode()

    with open(DB_FILE, "w") as file:
        json.dump({"salt": vault["salt"], "encrypted_data": encrypted_data}, file)




def main():
    console.print("[bold cyan] 💎 Welcome - Password Vault[/bold cyan]")


    master_pw = getpass.getpass("Enter Master Password: ").strip()
    if not master_pw:
        print("Master Password must be set!")
        return

    vault = load_vault(master_pw)
    if vault is None:
        input("\nPress Enter to close...")
        return

    while True:
        console.print("\n[bold underline]Main Menu[/bold underline]")
        print("\n1. See every Entry")
        print("2. Search Entry")
        print("3. Add Entry")
        print("4. Password Generator")
        print("5. Close")

        choice = input("Choose an Option (1-5): ").strip()


        if choice == "1":
            if not vault["entries"]:
                console.print("[yellow]No entries yet.[/yellow]")
                continue

            table = Table(title="All saved Entries", show_lines=True)
            table.add_column("Website / App Name", style="cyan", no_wrap=True)
            table.add_column("Email / Username", style="yellow")
            table.add_column("Password", style="magenta")
            table.add_column("Notes", style="green")

            for app, details in vault["entries"].items():
                table.add_row(
                    app,
                    details.get("username", "-"),
                    "••••••••",
                    details.get("notes", "-")
                )

            console.print(table)


        elif choice == "2":
            if not vault["entries"]:
                console.print("[yellow]No entries yet.[/yellow]")
                continue

            search_query = input("Enter Name: ").strip()
            if not search_query:
                console.print("[red]Search Term must be set![/red]")
                continue


            found_entries = {k: v for k, v in vault["entries"].items() if search_query.lower() in k.lower()}

            if not found_entries:
                console.print(f"[yellow]No Entry found for '{search_query}' gefunden.[/yellow]")
                continue

            table = Table(title=f"Search for '{search_query}'", show_lines=True)
            table.add_column("Website / App", style="cyan", no_wrap=True)
            table.add_column("Benutzername", style="yellow")
            table.add_column("Passwort", style="magenta")
            table.add_column("Notizen", style="green")

            for app, details in found_entries.items():
                table.add_row(
                    app,
                    details.get("username", "-"),
                    details.get("password", "-"),
                    details.get("notes", "-")
                )

            console.print(table)


        elif choice == "3":
            app_name = input("Name of Website / Programm: ").strip()
            if not app_name:
                console.print("[red]Name must be set![/red]")
                continue

            username = input("Username / Email: ").strip()


            password = getpass.getpass("Password (leave empty for random generated password): ").strip()

            if not password:
                password = generate_random_password()
                console.print(f"[bold green]Generated Password:[/bold green] {password}")

            notes = input("Notes (optional): ").strip()
            if not notes:
                notes = "-"

            vault["entries"][app_name] = {
                "username": username,
                "password": password,
                "notes": notes
            }

            save_vault(master_pw, vault)
            console.print(f"[bold green]✅ {app_name} was added![/bold green]")


        elif choice == "4":
            length_str = input("Password Length (Default 16): ").strip()
            length = int(length_str) if length_str.isdigit() else 16

            generated_pw = generate_random_password(length)

            console.print("\n--- Your random Passowrd ---")
            console.print(f"[bold select_background cyan]{generated_pw}[/bold select_background cyan]")
            console.print("------------------------------")


        elif choice == "5":
            console.print("[bold cyan]Programm closed[/bold cyan]")
            break

        else:
            console.print("[red]Invalid Option, enter 1, 2, 3, 4 or 5![/red]")

if __name__ == "__main__":
    main()