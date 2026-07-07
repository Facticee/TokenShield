from rich.console import Console
import secrets
import string
import json
import os

from rich.table import Table

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




    vault = load_vault()

    while True:
        print("\n1. See every Entry")
        print("2. Search Entry")
        print("3. Add Entry")
        print("4. Password Generator")
        print("5. Close")

        choice = input("Choice: ")

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
                table.add_row(app, details.get("username", "-"), "••••••••", details.get("notes", "-"))
            console.print(table)

        elif choice == "2":
            if not vault["entries"]:
                console.print("[yellow]No entries yet.[/yellow]")
                continue
            search_query = input("Enter Name: ").strip()
            found_entries = {k: v for k, v in vault["entries"].items() if search_query.lower() in k.lower()}

            if not found_entries:
                console.print(f"[yellow]No Entry found for '{search_query}'.[/yellow]")
                continue

            table = Table(title=f"Search for '{search_query}'", show_lines=True)
            table.add_column("Website / App Name", style="cyan", no_wrap=True)
            table.add_column("Email / Username", style="yellow")
            table.add_column("Password", style="magenta")
            table.add_column("Notes", style="green")

            for app, details in found_entries.items():
                table.add_row(app, details.get("username", "-"), details.get("password", "-"), details.get("notes", "-"))
            console.print(table)

        elif choice == "3":
            app_name = input("Name of Website / App: ").strip()
            username = input("Username / Email: ").strip()
            password = input("Password (leave empty for random generated password): ").strip()
            if not password:
                password = generate_random_password()
                console.print(f"[bold green]Generated Password:[/bold green] {password}")
            notes = input("Notes (optional): ").strip() or "-"

            vault["entries"][app_name] = {"username": username, "password": password, "notes": notes}
            save_vault(vault)
            console.print(f" {app_name} was added!")

        elif choice == "4":
            length_str = input("Password Length (Default 16): ").strip()
            length = int(length_str) if length_str.isdigit() else 16
            generated_pw = generate_random_password(length)
            console.print(f"\n---- Random Password ----\n {generated_pw} \n------------------------------")
        elif choice == "5":
            console.print("Programm closed.")
            break

        else:
            print("Test")

if __name__ == "__main__":
    main()
