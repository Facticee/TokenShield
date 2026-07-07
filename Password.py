from rich.console import Console

console = Console()

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
        else:
            print("Test")

if __name__ == "__main__":
    main()