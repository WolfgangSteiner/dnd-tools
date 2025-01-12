
import random

def roll_die(sides=20):
    return random.randint(1, sides)

def simulate_attack(attacker, defender):
    """
    Simulates an attack from an attacker to a defender.
    """
    print(f"{attacker['name']} attacks {defender['name']} ", end="")
    attack_roll = roll_die() + attacker['attack_bonus']
    if attack_roll >= defender['AC']:
        damage = sum(roll_die(d) for d in attacker['damage_dice']) + attacker['damage_bonus']
        defender['hp'] -= damage
        print(f" for {damage} points of damage")
    else:
        print(f" but misses")
        damage = 0
    return damage

def simulate_encounter(pcs, monsters):
    """
    Simulates a single encounter and returns the outcome.
    """
    participants = pcs + monsters
    random.shuffle(participants)

    while any(pc['hp'] > 0 for pc in pcs) and any(monster['hp'] > 0 for monster in monsters):
        for participant in participants:
            if participant['hp'] <= 0:
                continue

            if participant in pcs:
                target = random.choice([monster for monster in monsters if monster['hp'] > 0])
            else:
                target = random.choice([pc for pc in pcs if pc['hp'] > 0])

            simulate_attack(participant, target)

    pcs_alive = sum(pc['hp'] > 0 for pc in pcs)
    monsters_alive = sum(monster['hp'] > 0 for monster in monsters)

    return {
        'pcs_alive': pcs_alive,
        'monsters_alive': monsters_alive
    }

def calculate_difficulty(pcs, monsters, iterations=1000):
    """
    Simulates multiple encounters and calculates the encounter difficulty.
    """
    outcomes = {'pc_victories': 0, 'monster_victories': 0}

    for _ in range(iterations):
        # Create fresh copies of the participants for each simulation
        pcs_copy = [pc.copy() for pc in pcs]
        monsters_copy = [monster.copy() for monster in monsters]

        outcome = simulate_encounter(pcs_copy, monsters_copy)

        if outcome['pcs_alive'] > 0:
            outcomes['pc_victories'] += 1
        else:
            outcomes['monster_victories'] += 1

    pc_win_rate = outcomes['pc_victories'] / iterations
    difficulty = "Easy" if pc_win_rate > 0.75 else "Medium" if pc_win_rate > 0.5 else "Hard" if pc_win_rate > 0.25 else "Deadly"

    return {
        'pc_win_rate': pc_win_rate,
        'difficulty': difficulty,
        'outcomes': outcomes
    }

# Example usage:
pcs = [
    {'name': 'Fighter', 'hp': 30, 'AC': 16, 'attack_bonus': 5, 'damage_dice': [8], 'damage_bonus': 3},
    {'name': 'Wizard', 'hp': 18, 'AC': 12, 'attack_bonus': 4, 'damage_dice': [6, 6], 'damage_bonus': 2}
]

monsters = [
    {'name': 'Goblin', 'hp': 12, 'AC': 13, 'attack_bonus': 4, 'damage_dice': [6], 'damage_bonus': 2},
    {'name': 'Goblin', 'hp': 12, 'AC': 13, 'attack_bonus': 4, 'damage_dice': [6], 'damage_bonus': 2}
]

print("Starting encounter!")

results = calculate_difficulty(pcs, monsters, iterations=1)
print(results)
