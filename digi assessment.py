# --- Constants ---
STARTING_HEALTH = 100
INVENTORY_SIZE = 5

# --- Variables ---
player_inventory = []
current_room = "Entrance"

# --- Map ---
game_map = {
    "Entrance": {
        "description": "You stand before the gates of the Library of Babel, an infinite, universe-spanning library, containing every possible combination of letters and characters. Inside this library is every piece of knowledge, every secret, every lie, and also absolute gibberish.",
        "north": "Foyer",
        "item": "Blessed Inkwell",
    },
    "Foyer": {
        "description": "The centre of the Library, the Golden Quill rests here.",
        "south": "Entrance",
        "east": "Vault",
        "item": "Golden Quill",
    },
    "Vault": {
        "description": "Rows of books line the corridor leading to the vault. A heavy, locked door hides the secrets of the Library.",
        "west": "Foyer",
        "item": "Ink-Stained Book",
    },
}


while True:
    room_data = game_map[current_room]
    print ({room_data['description']})

    player_command = input("Please enter a command.")