
import os
import sys

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    """Print the main menu"""
    print("=" * 50)
    print("      FILE & FOLDER MANAGER")
    print("=" * 50)
    print("1. under construction X")
    print("2. Batch File Renamer")
    print("3. Duplicate File Finder")
    print("4. Exit")
    print("=" * 50)

def main():
    while True:
        clear_screen()
        print_menu()
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            continue
        elif choice == '2':
            from rename import batch_renamer
            batch_renamer()
        elif choice == '3':
            from duplicates import duplicate_finder
            duplicate_finder()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()