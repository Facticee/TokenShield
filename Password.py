import json
import os
import secrets
import string
import getpass
from rich.console import Console
from rich.table import Table

console = Console()
DB_FILE = "vault.json"


def load_vault(master_password: str) -> dict:
    if not os.path.exists(DB_FILE):
        return {"cipher": "VERSCHLÜSSELUNG_CIPHER", "entries": {}}

    with open(DB_FILE, "r") as f:
        data = json.load(f)

    # Passwort-Schutz-Prüfung im Klartext (Simuliert für den Übergang)
    if data.get("passwort_schutz") != master_password:
        console.print("\n[bold red]❌ Wrong password![/bold red]\n")
        return None

    return {"cipher": data.get("cipher", "VERSCHLÜSSELUNG_CIPHER"), "entries": data.get("entries", {})}

def save_vault(master_password: str, vault: dict):
    with open(DB_FILE, "w") as f:
        json.dump({
            "passwort_schutz": master_password,
            "cipher": vault["cipher"],
            "entries": vault["entries"]
        }, f, indent=4)

def generate_random_password(pwlength=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return "".join(secrets.choice(chars) for _ in range(pwlength))


def main():
    console.print("[bold cyan]💎 Welcome - Password Vault[/bold cyan]")

    master_pw = getpass.getpass("Master-Passwort eingeben: ").strip()
    if not master_pw:
        print("Master-Passwort darf nicht leer sein!")
        return

    vault = load_vault(master_pw)
    if vault is None:
        input("\nDrücke ENTER zum Beenden...")
        return

    while True:
        print("\n1. See every Entry")
        print("2. Search Entry")
        print("3. Add Entry")
        print("4. Password Generator")
        print("5. Close")

        choice = input("Choice: ").strip()

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
            if not search_query:
                console.print("[red]Suchbegriff darf nicht leer sein![/red]")
                continue

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
            if not app_name:
                console.print("[red]Name darf nicht leer sein![/red]")
                continue

            username = input("Username / Email: ").strip()

            password = getpass.getpass("Password (leave empty for random generated password): ").strip()
            if not password:
                password = generate_random_password()
                console.print(f"[bold green]Generated Password:[/bold green] {password}")

            notes = input("Notes (optional): ").strip() or "-"

            vault["entries"][app_name] = {"username": username, "password": password, "notes": notes}

            save_vault(master_pw, vault)
            console.print(f"✅ {app_name} was added!")

        elif choice == "4":
            length_str = input("Password Length (Default 16): ").strip()
            length = int(length_str) if length_str.isdigit() else 16
            generated_pw = generate_random_password(length)
            console.print(f"\n---- Random Password ----\n {generated_pw} \n------------------------------")

        elif choice == "5":
            console.print("Programm closed.")
            break
        else:
            console.print("[red]Ungültige Option, bitte 1, 2, 3, 4 oder 5 eingeben.[/red]")

if __name__ == "__main__":
    main()