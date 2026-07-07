from rich.console import Console
import secrets
import string

console = Console()

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

            print(generate_random_password(length))
        else:
            print("Test")

if __name__ == "__main__":
    main()
