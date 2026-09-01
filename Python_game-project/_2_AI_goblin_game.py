import random
import json

# ==========================================
# CONSTANTS & CONFIGURATION
# ==========================================
LEVEL_TABLE = {
    1: 0,
    2: 100,
    3: 200,
    4: 500,
    5: 1000,
    6: 2000,
    7: 5000,
    8: 10000,
    9: 15000,
    10: 25000
}

ENEMY_TEMPLATES = [
    ("Slime", 15, 25, 4, 7, 10),
    ("Wolf", 18, 28, 7, 10, 30),
    ("Skeleton", 20, 30, 5, 9, 24),
    ("Bandit", 22, 32, 6, 11, 38),
    ("Goblin", 25, 35, 6, 8, 20),
    ("Vampire", 28, 38, 9, 13, 50),
    ("Orc", 30, 40, 8, 12, 40),
    ("Troll", 35, 50, 10, 15, 50),
    ("Dragon", 40, 60, 12, 20, 100)
]

# Global store for successful runs
leaderboard = []

# ==========================================
# CLASSES & FUNCTIONS
# ==========================================
class Enemy:
    def __init__(self, name, min_health, max_health, min_attack, max_attack, xp):
        self.name = name
        self.min_health = min_health
        self.max_health = max_health
        self.min_attack = min_attack
        self.max_attack = max_attack
        self.xp = xp
        self.health = random.randint(min_health, max_health)

    def take_damage(self, damage):
        self.health -= damage

    def get_attack_damage(self):
        return random.randint(self.min_attack, self.max_attack)


def save_leaderboard(filename="scoreboard.json"):
    #Saves the global leaderboard to a JSON file.
    with open(filename, "w") as json_file:
        json.dump(leaderboard, json_file, indent=4)
    print(f"Leaderboard saved to {filename}!")


    #Whole leaderboard formatting was done by AI
def display_leaderboard():
    print("\n==========================================")
    print("           LEADERBOARD (SUCCESSFUL RUNS)   ")
    print("==========================================")

    sorted_board = sorted(leaderboard, key=lambda x: (x['level'], x['xp'], x['enemies']), reverse=True)

    print(f"{'Rank':<5} | {'Hero Name':<15} | {'LVL':<5} | {'XP':<7} | {'Kills':<6}")
    print("-" * 48)
    for idx, entry in enumerate(sorted_board, start=1):
        print(f"{idx:<5} | {entry['name']:<15} | {entry['level']:<5} | {entry['xp']:<7} | {entry['enemies']:<6}")
    print("==========================================\n")

# ==========================================
# MAIN GAME LOOP
# ==========================================
def start_game():
    print("Game started!")

    while True:
        user_input = input("Please enter your HERO name (or type 'q' to quit application):\n").strip()
        if user_input.lower() == 'q':
            print("Thanks for playing! Goodbye.")
            break
        elif not user_input:
            print("Name cannot be empty.")
            continue

        user_name = user_input

        # Initialize player stats
        player_max_hp = random.randint(100, 125)
        player_health = player_max_hp
        player_min_weapon = 5
        player_max_weapon = 9
        player_level = 1
        current_xp = 0
        next_level_xp = LEVEL_TABLE.get(player_level + 1)
        enemies_defeated = 0
        heal_fountain = 45

        run_active = True

        while player_health > 0 and run_active:
            if random.random() < 0.30:
                player_health += heal_fountain        
                if player_health > player_max_hp:
                    player_health = player_max_hp
                    
                print(f"\n+++ You discovered a Healing Fountain! +++")
                print(f"You recovered {heal_fountain} HP! (Current HP: {player_health}/{player_max_hp})")

            #Creating an encounter
            current_enemy = Enemy(*random.choice(ENEMY_TEMPLATES))

            #Also formatted by AI
            print(f"\n--- New Encounter ---")
            hero_str = f"{user_name} - LVL {player_level}  | HP: {player_health:<3} | DMG: {player_min_weapon}-{player_max_weapon} | XP: {current_xp} / {next_level_xp if next_level_xp else 'MAX'}"
            enemy_str = f"{current_enemy.name:<6} | HP: {current_enemy.min_health}-{current_enemy.max_health:<2} | DMG: {current_enemy.min_attack}-{current_enemy.max_attack} | XP: {current_enemy.xp}"

            print("┌────────────────────────────────────────────────────┐")
            print(f"│ {hero_str:<50} │")
            print("├────────────────────────────────────────────────────┤")
            print(f"│ {enemy_str:<50} │")
            print("└────────────────────────────────────────────────────┘")
            
            prompt = input("\nWould you like to attack? (y = attack, n = retire run, q = quit game): ").strip().lower()

            if prompt == 'q':
                print(f"\nExiting game. Thanks for playing!")
                return

            elif prompt == 'n':
                print(f"\nYou retired safely! Run finished with {enemies_defeated} enemies defeated.")
                leaderboard.append({
                    "name": user_name,
                    "level": player_level,
                    "xp": current_xp,
                    "enemies": enemies_defeated
                })
                display_leaderboard()
                save_leaderboard()  # <--- Save to JSON when retiring
                run_active = False

            elif prompt == 'y':
                while current_enemy.health > 0 and player_health > 0:
                    player_hit = random.randint(player_min_weapon, player_max_weapon)
                    current_enemy.take_damage(player_hit)
                    
                    enemy_display_hp = max(0, current_enemy.health)
                    print(f"You hit the {current_enemy.name} for {player_hit} DMG! ({enemy_display_hp} HP left)")
                    
                    if current_enemy.health > 0:
                        enemy_hit = current_enemy.get_attack_damage()
                        player_health -= enemy_hit
                        
                        player_display_hp = max(0, player_health)
                        print(f"The {current_enemy.name} hits you for {enemy_hit} DMG! ({player_display_hp} HP left)")

                if player_health <= 0:
                    print(f"\nYou were slain in battle! Game Over for {user_name}.")
                    print("Failed runs are not eligible for the leaderboard.")
                    display_leaderboard()
                    run_active = False
                else:
                    enemies_defeated += 1
                    current_xp += current_enemy.xp
                    print(f"\nYou defeated the {current_enemy.name}! Gained +{current_enemy.xp} XP.")

                    while next_level_xp and current_xp >= next_level_xp:
                        player_level += 1
                        player_max_hp += 15
                        player_health = int(min(player_max_hp, player_health + 0.5 * player_max_hp))
                        player_min_weapon += 2
                        player_max_weapon += 2

                        next_level_xp = LEVEL_TABLE.get(player_level + 1)

                        print(f"\n LEVEL UP! You reached Level {player_level}! ")
                        print(f"-> Max HP increased to {player_max_hp}. Restored up to 50% of MAX HP)")
                        print(f"-> Weapon Damage increased to {player_min_weapon}-{player_max_weapon}")

                    if player_level >= 10:
                        print(f"\n CONGRATULATIONS! You reached the MAXIMUM LEVEL ({player_level})!")
                        leaderboard.append({
                            "name": user_name,
                            "level": player_level,
                            "xp": current_xp,
                            "enemies": enemies_defeated
                        })
                        display_leaderboard()
                        save_leaderboard()  # <--- Save to JSON on max level win
                        run_active = False
            else:
                print("Invalid input! Please type 'y', 'n', or 'q'.")

#AI suggested this syntaxis as it helps with importing
if __name__ == "__main__":
    start_game()