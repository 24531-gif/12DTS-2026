import random
import time
import sys


# --- Constants ---
STARTING_HEALTH = 100
INVENTORY_SIZE = 5
STARTING_GOLD = 20
SHOP_ITEMS = [
    {"name": "Healing Scroll", "cost": 10, "type": "heal", "value": 20},
    {"name": "Lucky Charm", "cost": 15, "type": "buff", "value": 10},
]

# --- Variables ---
player_health = STARTING_HEALTH
player_inventory = []
current_room = "Entrance"
game_running = True
player_gold = STARTING_GOLD
puzzles_solved = 0
player_defence = 0

# --- Map ---
game_map = {
    "Entrance": {
        "description": "You stand before the infinite Library of Babel. Every book written, possible or impossible, exists here.",
        "north": "Foyer",
        "item": "Blessed Inkwell",
    },
    "Foyer": {
        "description": "The golden-lit centre. The Golden Quill rests on a pedestal.",
        "south": "Entrance",
        "north": "Cipher Room",
        "west": "Shop", 
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
    },
    "Shop": {
        "description": "A quiet librarian watches you. Knowledge has a price.",
        "east": "Foyer"
    },
    "Cipher Room": {
        "description": "A strange looking book lies open. The letters are scrambled.",
        "south": "Foyer",
        "cipher": True
    }
}


# --- Functions ---

def typewriter_print(text): # Aesthetic typewriter function
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(.01)
    print() # Adds a new line


def get_valid_input(prompt, valid_options): # Ensures the user's input is valid and prevents unwanted crashes
    while True:
        choice = input(prompt).lower().strip()
        if choice in valid_options:
            return choice
        print ("Invalid input. Please try again.")


def start_menu(): # Displays Start Menu and Instructions
    typewriter_print ("--------------------------------------")
    typewriter_print ("-- Welcome to the Library of Babel. --")
    typewriter_print ("--------------------------------------")
    typewriter_print ("Navigate the infinite shelves.")
    typewriter_print ("Uncover the ultimate truth.")
    typewriter_print ("Find the Golden Quill to unlock the vault.")
    typewriter_print ("--------------------------------------")
    typewriter_print ("Your adventure has begun...")
    typewriter_print ("Hint: type 'help' for a list of all player commands.")


def restart_game():
    global player_health, player_inventory, current_room, player_gold, puzzles_solved
    player_health = STARTING_HEALTH
    player_inventory = []
    current_room = "Entrance"
    player_gold = STARTING_GOLD
    puzzles_solved = 0


# --- Shop System ---


def shop():
    global player_gold, player_health

    while True:
        typewriter_print(f"\nGold: {player_gold}")

        for i, item in enumerate(SHOP_ITEMS):
            typewriter_print(f"{i+1}. {item['name']} - {item['cost']} gold")

        typewriter_print(f"{len(SHOP_ITEMS)+1}. Exit")

        valid_choices = [str(i+1) for i in range(len(SHOP_ITEMS)+1)]
        choice = get_valid_input("Choose: ", valid_choices)

        if choice == str(len(SHOP_ITEMS)+1):
            return

        item = SHOP_ITEMS[int(choice)-1]

        if player_gold >= item["cost"]:
            player_gold -= item["cost"]

            if item["type"] == "heal":
                player_health += item["value"]
                typewriter_print(f"You gained {item['value']} HP.")

            elif item["type"] == "buff":
                player_defence += item["value"]
                typewriter_print("You feel protected.")

        else:
            typewriter_print("Not enough gold.")


# --- Item Effects ---

def use_item(item):
    global player_health

    if item == "Blessed Inkwell":
        player_health = min(STARTING_HEALTH, player_health + 30)
        typewriter_print("You feel restored. (+30 HP)")

    elif item == "Ink-Stained Book":
        typewriter_print("The book whispers forbidden truths... You feel weaker. (-10 HP)")
        player_health -= 10

    elif item == "Golden Quill":
        typewriter_print("The Quill hums with power. Use it to unlock the Vault.")

    else:
        typewriter_print("Nothing happens.")



# --- Puzzle System ---

def solve_riddle():
    global puzzles_solved

    answer = input("I get wetter as you get drier: ").lower().strip()

    if answer == "towel":
        puzzles_solved += 1
        typewriter_print ("Correct. The path opens.")
        return True
    else:
        typewriter_print ("Incorrect.")
        return False



def solve_cipher():
    global puzzles_solved

    answer = input("Decode: Uifsf jt op tqppo: ").lower().strip()

    if answer == "there is no spoon":
        puzzles_solved += 1
        typewriter_print ("Correct. The book rearranges itself.")
        return True
    else:
        typewriter_print ("Incorrect. The book stays jumbled.")
        return False
    
# --- Random Events ---

def random_event():
    global player_health

    event_roll = random.randint(1, 4)

    if event_roll == 1:
        typewriter_print("A cursed sentence rearranges itself in your mind... (-5 HP)")
        player_health -= 5
        typewriter_print ("Hint: You can use the 'use' command to use items you have picked up.")

    elif event_roll == 2:
        typewriter_print("You find a helpful note scribbled in the margins. (+5 HP)")
        player_health += 5
        typewriter_print("Hint: You can use the 'help' command to see all player commands.")

# --- Combat ---

def encounter_enemy():
    global player_health, player_gold

    enemy_health = 20
    typewriter_print("A hostile Librarian appears!")

    while enemy_health > 0 and player_health > 0:
        action = input("Fight or run? ").lower()

        if action == "fight":
            damage = random.randint(5, 15)
            enemy_health -= damage
            typewriter_print(f"You deal {damage} damage.")

            if enemy_health > 0:
                enemy_damage = max(0, random.randint(5, 10) - player_defence)
                player_health -= enemy_damage
                typewriter_print(f"The Librarian hits you for {enemy_damage}!")

        elif action == "run":
            typewriter_print("You escape!")
            return
        else:
            typewriter_print("Invalid action.")

    if player_health <= 0:
        typewriter_print("You were defeated by the Librarian...")
    else:
        typewriter_print("You defeated the Librarian! (+5 gold)")
        player_gold += 5

# --- Game Loop ---

start_menu()

while game_running:

    room_data = game_map[current_room]


    typewriter_print("\n" + room_data["description"])
    typewriter_print(f"Health: {player_health}")

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
    if "cipher" in room_data:
        if not solve_cipher():
            continue
        else:
            del room_data["cipher"]


    if "item" in room_data:
        typewriter_print(f"You see a {room_data['item']} here.")

    command = get_valid_input("> ",
                    ["north", "south", "east", "west", "take", "use", "inventory", "help", "quit", "shop"])

    if command == "help":
        typewriter_print("Commands: north, south, east, west, take, use, inventory, quit, shop")

    elif command in ["north", "south", "east", "west"]:
        if command in room_data:
            next_room = room_data[command]

            # Check lock
            if "locked" in game_map[next_room] and game_map[next_room]["locked"]:
                if "Golden Quill" in player_inventory:
                    typewriter_print("The Quill unlocks the Vault!")
                    game_map[next_room]["locked"] = False
                else:
                    typewriter_print("The door is locked.")
                    continue

            current_room = next_room
        else:
            typewriter_print("You can't go that way.")

    elif command == "take":
        if "item" in room_data:
            if len(player_inventory) < INVENTORY_SIZE:
                item = room_data["item"]
                player_inventory.append(item)
                typewriter_print(f"You picked up the {item}.")
                del room_data["item"]
            else:
                typewriter_print("Inventory full.")
        else:
            typewriter_print("Nothing here.")

    elif command == "use":
        if player_inventory:
            typewriter_print(f"Inventory: {player_inventory}")
            item = input("Which item? ")
            if item in player_inventory:
                use_item(item)
                player_inventory.remove(item)
            else:
                typewriter_print("You don't have that.")
        else:
            typewriter_print("Inventory is empty.")

    elif command == "inventory":
        typewriter_print("Inventory:", player_inventory if player_inventory else "Empty")

    elif command == "quit":
        typewriter_print("Goodbye.")
        break

    elif command == "shop":
        if current_room == "Shop":
            shop()
        else:
            typewriter_print ("You must be in the shop.")

    else:
        typewriter_print("Invalid command.")
        
    # --- Win/Lose Conditions ---
    
    if player_health <= 0:
        typewriter_print("You collapse among the endless books... Game Over.")
        choice = get_valid_input("Restart? (Yes/No): ", ["yes", "no"])
        if choice == "yes":
            restart_game()
            continue
        else:
            break

    if current_room == "Vault" and "Golden Quill" in player_inventory and puzzles_solved == 2:
        typewriter_print("You unlock the ultimate truth of the Library - the real treasure was the friends you made along the way.")
        typewriter_print ("You win!")
        choice = get_valid_input("Play again? (Yes/No): ", ["yes", "no"])
        if choice == "yes":
            restart_game()
            continue
        else:
            break
