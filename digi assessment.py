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
        "east": "Vault",
        "item": "Golden Quill",
    },
    "Vault": {
        "description": "A locked vault door bars your way.",
        "west": "Foyer",
        "locked": True,
        "item": "Ink-Stained Book",
    },
}

# --- Item Effects ---
def use_item(item):
    global player_health

    if item == "Blessed Inkwell":
        player_health = min(STARTING_HEALTH, player_health + 30)
        print("You feel restored. (+30 HP)")

    elif item == "Ink-Stained Book":
        print("The book whispers forbidden truths... You feel weaker.")
        player_health -= 10

    elif item == "Golden Quill":
        print("The Quill hums with power. You feel destined.")

    else:
        print("Nothing happens.")

# --- Random Events ---
def random_event():
    global player_health

    event_roll = random.randint(1, 4)

    if event_roll == 1:
        print("A cursed sentence rearranges itself in your mind...")
        player_health -= 5

    elif event_roll == 2:
        print("You find a helpful note scribbled in the margins. (+5 HP)")
        player_health += 5

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
while game_running:
    room_data = game_map[current_room]

    print("\n" + room_data["description"])
    print(f"Health: {player_health}")

    # Random chance of encounter
    if random.random() < 0.3:
        encounter_enemy()

    # Random world event
    if random.random() < 0.3:
        random_event()

    if "item" in room_data:
        print(f"You see a {room_data['item']} here.")

    command = input("> ").lower()

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
        break

    if current_room == "Vault" and "Golden Quill" in player_inventory:
        print("You unlock the ultimate truth of the Library. You win!")
        break
