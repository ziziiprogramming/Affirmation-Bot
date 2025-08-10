import json
import random
import os
from datetime import datetime
from cryptography.fernet import Fernet

DEFAULT_FILE = "default_affirmations.json"
COMMUNITY_FILE = "community_affirmations.json"
PERSONAL_FILE = "personal_affirmations.json.enc"
KEY_FILE = "key.key"

def load_key():
    """Load or generate encryption key for personal affirmations."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return key

key = load_key()
fernet = Fernet(key)

def encrypt_data(data: str) -> bytes:
    return fernet.encrypt(data.encode())

def decrypt_data(data: bytes) -> str:
    return fernet.decrypt(data).decode()

def load_affirmations(file_path, encrypted=False):
    """Load affirmations from a file, decrypt if necessary."""
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'rb' if encrypted else 'r') as file:
            if encrypted:
                data = decrypt_data(file.read())
                return json.loads(data).get("affirmations", [])
            else:
                data = json.load(file)
                return data.get("affirmations", [])
    except (json.JSONDecodeError, ValueError):
        return []

def save_affirmations(file_path, affirmations, encrypted=False):
    """Save affirmations to a file, encrypt if necessary."""
    data = json.dumps({"affirmations": affirmations}, indent=2)
    with open(file_path, 'wb' if encrypted else 'w') as file:
        if encrypted:
            file.write(encrypt_data(data))
        else:
            file.write(data if not encrypted else encrypt_data(data))

def show_random_affirmation(affirmations, source):
    if not affirmations:
        print(f"\n❌ No affirmations found in {source}.\n")
    else:
        affirmation = random.choice(affirmations)
        print(f"\n🌼 {source} Affirmation:\n> {affirmation}\n")

def add_to_community():
    name = input("\n📝 Your Name (optional): ").strip() or "Anonymous"
    affirmation = input("💬 Share your gentle affirmation for others: ").strip()

    if not affirmation:
        print("❌ Affirmation cannot be empty.\n")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f'"{affirmation}" — {name}, {timestamp}'

    affirmations = load_affirmations(COMMUNITY_FILE)
    affirmations.append(entry)
    save_affirmations(COMMUNITY_FILE, affirmations)
    print("✅ Thank you for contributing to the community! 🌟\n")

def add_to_personal():
    print("\n💗 This space is private and encrypted.")
    affirmation = input("🕊️ What would you like to tell yourself today?\n> ").strip()

    if not affirmation:
        print("❌ Affirmation cannot be empty.\n")
        return

    affirmations = load_affirmations(PERSONAL_FILE, encrypted=True)
    affirmations.append(affirmation)
    save_affirmations(PERSONAL_FILE, affirmations, encrypted=True)
    print("✅ Saved to your private encrypted vault. 🌸\n")

def main():
    print("🔒 This bot respects your privacy. Personal affirmations are encrypted.")
    print("📚 Responsible AI: No data is sent online. Everything stays on your device.\n")

    while True:
        print("\n🌷 Gentle Affirmation Bot 🌷")
        print("1. View a Default Affirmation")
        print("2. Read a Community-Contributed Affirmation")
        print("3. Contribute an Affirmation to the Community")
        print("4. View or Add Your Personal Affirmations (Encrypted)")
        print("5. Exit")

        choice = input("➤ Choose an option (1–5): ").strip()

        if choice == "1":
            affirmations = load_affirmations(DEFAULT_FILE)
            show_random_affirmation(affirmations, "Default")

        elif choice == "2":
            affirmations = load_affirmations(COMMUNITY_FILE)
            show_random_affirmation(affirmations, "Community")

        elif choice == "3":
            add_to_community()

        elif choice == "4":
            while True:
                print("\n💖 Personal Affirmations (Encrypted)")
                print("a. View a Random Personal Affirmation")
                print("b. Add a New Personal Affirmation")
                print("c. Back to Main Menu")

                sub_choice = input("➤ Choose an option (a/b/c): ").strip().lower()

                if sub_choice == "a":
                    affirmations = load_affirmations(PERSONAL_FILE, encrypted=True)
                    show_random_affirmation(affirmations, "Personal (Encrypted)")
                elif sub_choice == "b":
                    add_to_personal()
                elif sub_choice == "c":
                    break
                else:
                    print("❌ Invalid input. Please choose a/b/c.")

        elif choice == "5":
            print("\n🌸 Thank you for spending time with yourself today. 🌸")
            break

        else:
            print("❌ Invalid choice. Please enter 1–5.")

if __name__ == "__main__":
    main()
