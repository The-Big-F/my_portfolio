import random

# ==========================================
# CONSTANTS & CONFIGURATION
# ==========================================
LEVEL_TABLE = {
    1: 0,
    2: 100,
    3: 200,
    4: 500,
    5: 100,
    6: 2000,
    7: 5000,
    8: 10000,
    9: 1500,
    10: 25000
}

# Pre-defined enemy templates (reused across encounters)
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

# ==========================================
# CLASSES
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

# ==========================================
# GAME STATE INITIALIZATION
# ==========================================
player_max_hp = random.randint(100, 125)
player_health = player_max_hp
player_min_weapon = 5
player_max_weapon = 9
player_level = 1
current_xp = 0
next_level_xp = LEVEL_TABLE.get(player_level + 1)
enemies_defeated = 0
heal_fountain = 45


print("Game started!")

user_name = input(f"Please enter your HERO name\n")

while player_health > 0:
    
    # 30% chance for a Healing Fountain event
    if random.random() < 0.30:
        player_health += heal_fountain        
        if player_health > player_max_hp:
            player_health = player_max_hp
            
        print(f"\n+++ You discovered a Healing Fountain! +++")
        print(f"You recovered {heal_fountain} HP! (Current HP: {player_health}/{player_max_hp})")
        continue

    # Spawn an enemy from templates
    current_enemy = Enemy(*random.choice(ENEMY_TEMPLATES))

    print(f"\n--- New Encounter ---")
    
    # Format content lines to exact width (40 chars wide inside borders)
    hero_str = f"{user_name} - LVL {player_level}  | HP: {player_health:<3} | DMG: {player_min_weapon}-{player_max_weapon} | XP: {current_xp} / {next_level_xp}"
    enemy_str = f"{current_enemy.name:<6} | HP: {current_enemy.min_health}-{current_enemy.max_health:<2} | DMG: {current_enemy.min_attack}-{current_enemy.max_attack} | XP: {current_enemy.xp}"

    print("┌────────────────────────────────────────────────────┐")
    print(f"│ {hero_str:<50} │")
    print("├────────────────────────────────────────────────────┤")
    print(f"│ {enemy_str:<50} │")
    print("└────────────────────────────────────────────────────┘")
    
    prompt = input("\nWould you like to attack? (y/n, or press 'q' to quit): ").strip().lower()

    if prompt in ['n', 'q']:
        print(f"You quit the game. Thanks for playing! You have defeated {enemies_defeated} enemies.")
        break
    elif prompt == 'y':
        # Combat loop
        while current_enemy.health > 0 and player_health > 0:
            player_hit = random.randint(player_min_weapon, player_max_weapon)
            current_enemy.take_damage(player_hit)
            
            enemy_display_hp = current_enemy.health if current_enemy.health > 0 else 0
            print(f"You hit the {current_enemy.name} for {player_hit} DMG! ({enemy_display_hp} HP left)")
            
            if current_enemy.health > 0:
                enemy_hit = current_enemy.get_attack_damage()
                player_health -= enemy_hit
                
                player_display_hp = player_health if player_health > 0 else 0
                print(f"The {current_enemy.name} hits you for {enemy_hit} DMG! ({player_display_hp} HP left)")

        if player_health <= 0 and current_enemy.health <= 0:
            print(f"\nYou traded fatal blows and both perished! Game Over.")
            break
        elif player_health <= 0:
            print(f"\nYou were slain by the {current_enemy.name}. Game over.")
            break
        else:
            print(f"\nYou defeated the {current_enemy.name}! Your HP remains at {player_health}.")
            enemies_defeated += 1
            current_xp += current_enemy.xp
            print(f"\nYou defeated the {current_enemy.name}! Gained +{current_enemy.xp} XP.")

            # Level-up check
            while next_level_xp and current_xp >= next_level_xp:
                player_level += 1
                player_max_hp += 15
                player_health = int(min(player_max_hp, player_health + 0.5 * player_max_hp))
                player_min_weapon += 2
                player_max_weapon += 2

                # Update target threshold for subsequent level
                next_level_xp = LEVEL_TABLE.get(player_level + 1)

                print(f"\n LEVEL UP! You reached Level {player_level}! ")
                print(f"-> Max HP increased to {player_max_hp}. Restored up to 50% of the MAX HP)")
                print(f"-> Weapon Damage increased to {player_min_weapon}-{player_max_weapon}")            
    else:
        print("Invalid input! Please type 'y', 'n', or 'q'.")