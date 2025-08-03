import json
import random
import os
from datetime import datetime

# File paths
DEFAULT_FILE = "default_affirmations.json"
COMMUNITY_FILE = "community_affirmations.json"
PERSONAL_FILE = "personal_affirmations.json"

# Load affirmations from a file
def load_affirmations(file_path):
    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
            return data.get("affirmations", [])
        except json.JSONDecodeError:
            # If file is empty or corrupted, return an empty list
            return []


# Save affirmations to a file
def save_affirmations(file_path, affirmations):
    with open(file_path, "w") as file:
        json.dump({"affirmations": affirmations}, file, indent=2)

# Show a random affirmation from a given list
def show_random_affirmation(affirmations, source):
    if not affirmations:
        print(f"\n❌ No affirmations found in {source}.\n")
    else:
        affirmation = random.choice(affirmations)
        print(f"\n🌼 {source} Affirmation:\n> {affirmation}\n")

# Add to community affirmations
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

# Add to personal affirmations
def add_to_personal():
    print("\n💗 This space is just for you.")
    affirmation = input("🕊️ What would you like to tell yourself today?\n> ").strip()

    if not affirmation:
        print("❌ Affirmation cannot be empty.\n")
        return

    affirmations = load_affirmations(PERSONAL_FILE)
    affirmations.append(affirmation)
    save_affirmations(PERSONAL_FILE, affirmations)
    print("✅ Saved to your private collection. 🌸\n")

# Show menu
def main():
    while True:
        print("\n🌷 Gentle Affirmation Bot 🌷")
        print("1. View a Default Affirmation")
        print("2. Read a Community-Contributed Affirmation")
        print("3. Contribute an Affirmation to the Community")
        print("4. View or Add Your Personal Affirmations")
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
                print("\n💖 Personal Affirmations")
                print("a. View a Random Personal Affirmation")
                print("b. Add a New Personal Affirmation")
                print("c. Back to Main Menu")

                sub_choice = input("➤ Choose an option (a/b/c): ").strip().lower()

                if sub_choice == "a":
                    affirmations = load_affirmations(PERSONAL_FILE)
                    show_random_affirmation(affirmations, "Personal")
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
