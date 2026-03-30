import random

# --- Constants ---
STARTING_HEALTH = 100
INVENTORY_SIZE = 5

# --- Variables ---
player_health = STARTING_HEALTH
player_inventory = []
current_room = "Entrance"
game_running = True

# --- Map ---
game_map = {
    "Entrance": {
        "description": "You stand before the infinite Library of Babel. Knowledge and madness await.",
        "north": "Foyer",
        "item": "Blessed Inkwell",
    },
    "Foyer": {
        "description": "The golden-lit centre. The Golden Quill rests on a pedestal.",
        "south": "Entrance",
        "east": "Puzzle Room",
        "item": "Golden Quill",
    },
    "Vault": {
        "description": "A locked vault door bars your way.",
        "south": "Puzzle Room",
        "locked": True,
        "item": "Ink-Stained Book",
    },
    "Puzzle Room": {
        "description": "Runes glow on the walls of the Puzzle Room. A riddle blocks your path.",
        "west": "Foyer",
        "north": "Vault",
        "puzzle": True
    }
}


# --- Functions ---

def get_valid_input(prompt, valid_options): # Ensures the user's input is valid and prevents unwanted crashes
    while True:
        choice = input(prompt).lower().strip()
        if choice in valid_options:
            return choice
        print ("Invalid input. Please try again.")

def start_menu(): # Displays Start Menu and Instructions
    print("--------------------------------------")
    print("-- Welcome to the Library of Babel. --")
    print("--------------------------------------")
    print("Navigate the infinite shelves.")
    print("Uncover the ultimate truth.")
    print("Find the Golden Quill to unlock the vault.")
    print("--------------------------------------")
    input("PRESS 'ENTER' TO BEGIN")
    print("Your adventure has begun...")

def restart_game():
    global player_health, player_inventory, current_room
    player_health = STARTING_HEALTH
    player_inventory = []
    current_room = "Entrance"

# --- Item Effects ---
def use_item(item):
    global player_health

    if item == "Blessed Inkwell":
        player_health = min(STARTING_HEALTH, player_health + 30)
        print("You feel restored. (+30 HP)")

    elif item == "Ink-Stained Book":
        print("The book whispers forbidden truths... You feel weaker. (-10 HP)")
        player_health -= 10

    elif item == "Golden Quill":
        print("The Quill hums with power. Use it to unlock the Vault.")

    else:
        print("Nothing happens.")



# --- Puzzle System ---

def solve_riddle():
    print ("A voice whispers to you in your mind...")
    print ("I get wetter as you get drier. What am I?")
    answer = input("Your answer:").lower().strip()  # Makes sure multiple possible inputs are all valid

    if answer == "towel":
        print ("Correct. The path opens.")
        return True
    else:
        print ("Incorrect. The walls are sealed.")
        return False


# --- Random Events ---
def random_event():
    global player_health

    event_roll = random.randint(1, 4)

    if event_roll == 1:
        print("A cursed sentence rearranges itself in your mind... (-5 HP)")
        player_health -= 5
        print ("Hint: You can use the 'use' command to use items you have picked up.")

    elif event_roll == 2:
        print("You find a helpful note scribbled in the margins. (+5 HP)")
        player_health += 5
        print("Hint: You can use the 'help' command to see all player commands.")

# --- Combat ---
def encounter_enemy():
    global player_health

    enemy_health = 20
    print("A hostile Librarian appears!")

    while enemy_health > 0 and player_health > 0:
        action = input("Fight or run? ").lower()

        if action == "fight":
            damage = random.randint(5, 15)
            enemy_health -= damage
            print(f"You deal {damage} damage.")

            if enemy_health > 0:
                enemy_damage = random.randint(5, 10)
                player_health -= enemy_damage
                print(f"The Librarian hits you for {enemy_damage}!")

        elif action == "run":
            print("You escape!")
            return
        else:
            print("Invalid action.")

    if player_health <= 0:
        print("You were defeated by the Librarian...")
    else:
        print("You defeated the Librarian!")

# --- Game Loop ---

start_menu()

while game_running:

    room_data = game_map[current_room]


    print("\n" + room_data["description"])
    print(f"Health: {player_health}")

    # Random chance of encounter
    if random.random() < 0.2:
        encounter_enemy()

    # Random world event
    if random.random() < 0.1:
        random_event()

    if "puzzle" in room_data:
        if not solve_riddle():
            continue
        else:
            del room_data["puzzle"]

    if "item" in room_data:
        print(f"You see a {room_data['item']} here.")

    command = get_valid_input("> ",
                    ["north", "south", "east", "west", "take", "use", "inventory", "help", "quit"])

    if command == "help":
        print("Commands: north, south, east, west, take, use, inventory, quit")

    elif command in ["north", "south", "east", "west"]:
        if command in room_data:
            next_room = room_data[command]

            # Check lock
            if "locked" in game_map[next_room] and game_map[next_room]["locked"]:
                if "Golden Quill" in player_inventory:
                    print("The Quill unlocks the Vault!")
                    game_map[next_room]["locked"] = False
                else:
                    print("The door is locked.")
                    continue

            current_room = next_room
        else:
            print("You can't go that way.")

    elif command == "take":
        if "item" in room_data:
            if len(player_inventory) < INVENTORY_SIZE:
                item = room_data["item"]
                player_inventory.append(item)
                print(f"You picked up the {item}.")
                del room_data["item"]
            else:
                print("Inventory full.")
        else:
            print("Nothing here.")

    elif command == "use":
        if player_inventory:
            print("Inventory:", player_inventory)
            item = input("Which item? ")
            if item in player_inventory:
                use_item(item)
                player_inventory.remove(item)
            else:
                print("You don't have that.")
        else:
            print("Inventory is empty.")

    elif command == "inventory":
        print("Inventory:", player_inventory if player_inventory else "Empty")

    elif command == "quit":
        print("Goodbye.")
        break

    else:
        print("Invalid command.")

    # --- Win/Lose Conditions ---
    if player_health <= 0:
        print("You collapse among the endless books... Game Over.")
        choice = get_valid_input("Restart? (Yes/No): ", ["yes", "no"])
        if choice == "yes":
            continue
        else:
            break

    if current_room == "Vault" and "Golden Quill" in player_inventory:
        print("You unlock the ultimate truth of the Library - the real treasure was the friends you made along the way.")
        print ("You win!")
        choice = get_valid_input("Play agan? (Yes/No): ", ["yes", "no"])
        if choice == "yes":
            continue
        else:
            break




