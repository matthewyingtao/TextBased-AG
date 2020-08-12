import os
import random
from math import ceil, log, sqrt
import pickle

from colorama import Fore
from emoji import emojize

from implicits import implicits
from monsters import gargantuan_monsters, huge_monsters, large_monsters, medium_monsters, small_monsters, tiny_monsters

tier_attributes = {
    "gargantuan_monsters": [50, 40, 10, 800, 1000],
    "huge_monsters": [30, 9, 25, 400, 550],
    "large_monsters": [25, 15, 5, 180, 250],
    "medium_monsters": [18, 10, 4, 80, 120],
    "small_monsters": [13, 3, 3, 40, 80],
    "tiny_monsters": [8, 0, 2, 20, 40]
}

# this is the stats of the attacks for when you are fighting monsters
attacks = {
    "Slash": [3, 0.9, 0.1, 0],
    "Fireball": [4, 0.7, 0.25, 1],
    "Shock": [2, 1, 0.5, 1]
}

# list of equippable items
equips = {
    "Sword": [0, 0, 1, 0],
    "Body Armour": [1, 0, 0, 1],
    "Helmet": [2, 0, 0, 1],
    "Ring": [0, 1, 1, 0]
}

materials = {
    "Iron": 1,
    "Bronze": 1.5,
    "Silver": 2,
    "Gold": 2.5,
    "Platinum": 3,
    "Diamond": 4
}

# list of monster lists by difficulty
monster_tiers = [
    tiny_monsters, small_monsters, medium_monsters, large_monsters,
    huge_monsters, gargantuan_monsters
]

monster_tiers_names = [
    "tiny_monsters", "small_monsters", "medium_monsters", "large_monsters",
    "huge_monsters", "gargantuan_monsters"
]
weights = [50, 30, 20, 10, 5, 1]

# convert dictionaries to lists to use as keys
implicits_list = list(implicits.keys())
attacks_list = list(attacks.keys())
equips_list = list(equips.keys())
materials_list = list(materials.keys())


# clear screen
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


# pass arguments to print multiple strings in a certain color
def color_print(color, *args):
    for string in args:
        print(f"{color}{string}")
    print(f"{Fore.RESET}")


# handles all numeric inputs
def input_handler(max_input, *strings):
    for string in strings:
        print(string)
    while True:
        try:
            user_input = int(input(f"Input (0-{max_input}): "))
            if user_input < 0 or user_input > max_input:
                color_print(Fore.RED,
                            f"Input must be between 0 and {max_input}")
            elif user_input == 0:
                confirm = input("Are you sure?\n"
                                "-1- Quit\n"
                                "-any key- cancel\n")
                if confirm.lower() == "1":
                    raise SystemExit
            else:
                print()
                return user_input
        except ValueError:
            color_print(Fore.RED, "Enter a number!")


def show_options(*strings):
    options = []
    for index, string in enumerate(strings):
        options.append(emojize(f"-{index + 1}- {string}"))
    return options


def loot(difficulty):
    loot_weight = [
        (weight * (index**monster_tiers_names.index(difficulty) + 1))
        for index, weight in enumerate(weights)
    ]
    if random.choice((True, False)):
        item_type = random.choice(equips_list)
        item_material = random.choices(materials_list, weights=loot_weight)[0]
        player.inventory.append(Equipment(item_material, item_type))
        if random.choice((False, True)):
            player.inventory[-1].roll_mod()
        print(f"{player.inventory[-1].name} has dropped")
    else:
        print("No loot dropped")


def damage_calc(attacker, move, defender):
    # get random float between 0-1 and check for miss
    miss = random.random()
    attack = attacker.attack + attacks.get(move)[0]
    if miss < attacks.get(move)[1]:
        damage = ceil(attack - (defender.defence / sqrt(attack)))
        if damage < 1:
            damage = 0
        # get random float between 0-1 and check for critical hit, doubles damage if true
        critical_hit = random.random()
        if critical_hit < attacks.get(move)[2]:
            damage *= 2
            color_print(Fore.GREEN, "Critical Hit!")
        # calculate damage
        defender.health[0] -= damage
        color_print(
            Fore.RED,
            f"{attacker.name} used {move} and dealt {damage} damage to {defender.name}"
        )
    else:
        print("Miss!")


# check if the attack selection exists or can be used
def attack_check():
    for index, action in enumerate(attacks.keys()):
        print(f"-{index + 1}- {action}")
    print()
    while True:
        selection = input_handler((len(attacks))) - 1
        # check if player has enough mana to use
        if player.mana[0] - attacks.get(attacks_list[selection])[3] < 0:
            color_print(Fore.RED, "not enough mana!")
        else:
            break
    player.mana[0] -= attacks.get(attacks_list[selection])[3]
    return selection


# chooses the difficulty of adventure
def adventure():
    difficulty = input_handler(
        7, "Which dungeon?\n",
        *show_options("The Plains :bug:", "The Forest :evergreen_tree:",
                      "The Caves :gem_stone:",
                      "The Magic Forest :crystal_ball:",
                      "The Bay :water_wave:", "Hell :fire:", "Cancel"))
    if difficulty != 7:
        cls()
        return Monster(monster_tiers[difficulty - 1],
                       monster_tiers_names[difficulty - 1])


# battle function for when you fight a monster
def battle(combat_monster):
    while combat_monster.health[0] > 0 and player.health[0] > 0:
        combat_monster.stats()
        damage_calc(player, attacks_list[attack_check()], combat_monster)
        if combat_monster.health[0] > 0:
            damage_calc(combat_monster, attacks_list[0], player)
    if combat_monster.health[0] < 1:
        cls()
        color_print(Fore.GREEN, f"You have defeated {combat_monster.name}")
        player.xp[0] += combat_monster.xp
        player.xp_check()
        player.gold += round(
            tier_attributes.get(monster.tier)[4] * random.uniform(0.8, 1.2))
        loot(combat_monster.tier)
    elif player.health[0] < 1:
        color_print(Fore.RED, f"{combat_monster.name} has defeated you")


def get_base_stats(item_type):
    base_stats = equips.get(item_type)
    return base_stats


# used to print the stats of an object
def print_stats(**stats):
    stats_list = []
    for attribute, value in stats.items():
        stats_list.append(f"{attribute}: {value}")
    color_print(Fore.GREEN, "STATS:", *stats_list)


def save_player():
    # open player save file and dump the current player object
    save_name = input("Save name:")
    with open(f"saves/{save_name}.obj", 'wb') as player_file:
        pickle.dump(player, player_file)
    cls()
    color_print(Fore.GREEN, "Game saved!")


def load_player():
    # load player save file and set player to the loaded object
    save_files = [file for file in os.listdir("saves")]
    load = input_handler(len(save_files), *show_options(*save_files)) - 1
    player_load = open(f"saves/{save_files[load]}", 'rb')
    cls()
    color_print(Fore.GREEN, "Game loaded!")
    return pickle.load(player_load)


def delete_save():
    save_files = [file for file in os.listdir("saves")]
    delete = input_handler(
        len(save_files), "Which file would you like to delete?",
        *show_options(*save_files)) - 1
    os.remove(f"saves/{save_files[delete]}")


def manage_saves():
    save_action = input_handler(
        4, *show_options("Save game", "Load game", "Delete save", "Cancel"))
    if save_action == 1:
        save_player()
        return False
    elif save_action == 2:
        return True
    elif save_action == 3:
        delete_save()
        return False


def inn():
    if player.gold > player.inn_cost:
        player.gold -= player.inn_cost
        player.inn_cost = round(player.inn_cost * 1.5)
        player.health[0] = player.health[1]
        player.mana[0] = player.mana[1]
    else:
        print("Not enough gold!")
    player.stats()


class Equipment:
    def __init__(self, material, equip_type):
        self.name = material + " " + equip_type
        self.type = equip_type
        base_stats = [
            ceil(materials.get(material) * stat)
            for stat in (get_base_stats(equip_type))
        ]
        self.health = base_stats[0]
        self.mana = base_stats[1]
        self.attack = base_stats[2]
        self.defence = base_stats[3]
        self.mod = None
        self.mod_effect = [0, 0, 0, 0]
        self.isEquipped = False

    # Apply mod changes in stats
    def change_stats(self, operation):
        change = [(operation * effect) for effect in self.mod_effect]
        self.health += change[0]
        self.mana += change[1]
        self.attack += change[2]
        self.defence += change[3]

    # remove mod from an item's stats
    def remove_mod(self):
        if self.mod:
            self.name = self.name[len(self.mod) + 1:]
        self.change_stats(-1)
        self.mod = None
        self.mod_effect = [0, 0, 0, 0]

    # roll new mod on item
    def roll_mod(self):
        self.remove_mod()
        self.mod = implicits_list[random.randint(0, len(implicits_list) - 1)]
        self.mod_effect = implicits.get(self.mod)
        self.name = f"{self.mod} {self.name}"
        self.change_stats(1)

    def stats(self):
        print_stats(
            Name=self.name,
            Health=self.health,
            Mana=self.mana,
            Attack=self.attack,
            Defence=self.defence,
            Mod=self.mod_effect,
            Equipped=self.isEquipped)


class Character:
    def __init__(self, player_name):
        self.name = player_name
        self.health = [10, 10]
        self.mana = [5, 5]
        self.attack = 3
        self.defence = 0
        self.xp = [0, 50]
        self.level = 1
        self.gold = 0
        self.inventory = []
        self.inventory.append(Equipment("Iron", "Sword"))
        self.equipment = []
        self.inn_cost = 50

    def stats(self):
        print_stats(
            Name=self.name,
            Health=self.health,
            Mana=self.mana,
            Attack=self.attack,
            Defence=self.defence,
            XP=self.xp,
            Level=self.level,
            Gold=self.gold)

    # allocation of stat points
    def level_up(self):
        points = 3
        while points > 0:
            allocate = input_handler(
                4, "Allocate points:\n",
                *show_options("HEALTH", "MANA", "ATTACK", "DEFENCE"))
            if allocate == 1:
                self.health[1] += 1
            elif allocate == 2:
                self.mana[1] += 1
            elif allocate == 3:
                self.attack += 1
            elif allocate == 4:
                self.defence += 1
            points -= 1

    # check xp after battle, and increases the xp requirement for the next level
    def xp_check(self):
        if self.xp[0] > self.xp[1]:
            self.level += 1
            self.xp[0] -= self.xp[1]
            # XP to next level follows a logarithmic curve base 10 multiplier.
            self.xp[1] = round((log(self.level, 10) + 1) * self.xp[1], 0)
            color_print(Fore.GREEN, "You've leveled up!")
            self.level_up()
            self.xp_check()

    def show_inventory(self):
        print("INVENTORY:")
        # make list of names from inventory items before printing
        for item in self.inventory:
            print(
                f"({self.inventory.index(item) + 1}) {item.name}  ({Fore.LIGHTBLUE_EX}{item.health}, {item.mana}, {item.attack}, {item.defence}{Fore.RESET})"
            )
        print()
        inventory_action = input_handler(
            4, "What would you like to do? \n",
            *show_options("Re-roll modifier", "Equip item", "Inspect item",
                          "Cancel\n"))
        if inventory_action != 4:
            select_item = input_handler(len(self.inventory), "Which item?") - 1
        if inventory_action == 1:
            if self.inventory[select_item].isEquipped:
                color_print(Fore.RED, "Can't re-roll while equipped")
            else:
                cls()
                self.inventory[select_item].roll_mod()
                self.inventory[select_item].stats()
                color_print(Fore.GREEN, "Mod re-rolled")
        elif inventory_action == 2:
            cls()
            self.equip_item(self.inventory[select_item])
        elif inventory_action == 3:
            cls()
            self.inventory[select_item].stats()

    # check if an item is equipped before adding/removing stats
    def equip_item(self, item):
        if item.isEquipped:
            multiplier = -1
            print(f"You have unequipped {item.name}\n")
            self.equipment.remove(item.type)
        # check if an item of same type is equipped
        elif not (item.type in self.equipment):
            multiplier = 1
            print(f"You have equipped {item.name}\n")
            self.equipment.append(item.type)
        else:
            print("You already have an item of the same type equipped!\n")
            multiplier = 0
        self.health[0] += item.health * multiplier
        self.health[1] += item.health * multiplier
        self.mana[0] += item.mana * multiplier
        self.mana[1] += item.mana * multiplier
        self.attack += item.attack * multiplier
        self.defence += item.defence * multiplier
        item.isEquipped = not item.isEquipped


class Monster:
    def __init__(self, tier_list, tier):
        self.name = random.choice(list(tier_list))
        self.tier = tier
        self.health = [
            tier_attributes.get(tier)[0],
            tier_attributes.get(tier)[0]
        ]
        self.attack = tier_attributes.get(tier)[1]
        self.defence = tier_attributes.get(tier)[2]
        self.xp = round(
            tier_attributes.get(tier)[3] * random.uniform(0.8, 1.2))

    def stats(self):
        print_stats(
            Name=self.name,
            Health=self.health,
            Attack=self.attack,
            Defence=self.defence)


def training_board(**attributes):
    for attribute, value in attributes.items():
        training = value * emojize(":green_square:")
        for i in range(10 - len(training)):
            training += emojize(":white_large_square:")
        print(f" {training}  - {attribute}")


def training_cost(attribute):
    return 50 + (attribute * 80)


def gold_check(training):
    cost = training_cost(training)
    if training > 9:
        print("Already max level!")
        return False
    elif player.gold >= cost:
        return True
    else:
        print("You don't have enough gold!")
    return False


def potion_shop():
    pass


class Shop:
    def __init__(self):
        self.health = 0
        self.mana = 0
        self.attack = 0
        self.defence = 0
        # emoji names :green_square:   :white_large_square:

    def training(self):
        while True:
            cls()
            training_board(
                Health=self.health,
                Mana=self.mana,
                Attack=self.attack,
                Defence=self.defence)
            train = input_handler(
                5, "What would you like to train in?\n",
                *show_options(f"Health (Cost:{training_cost(self.health)})",
                              f"Mana (Cost:{training_cost(self.mana)})",
                              f"Attack (Cost:{training_cost(self.attack)})",
                              f"Defence (Cost:{training_cost(self.defence)})",
                              "Go back"))
            if train == 1:
                if gold_check(self.health):
                    player.gold -= training_cost(self.health)
                    self.health += 1
                    player.health[1] += 1
            elif train == 2:
                if gold_check(self.mana):
                    player.gold -= training_cost(self.mana)
                    self.mana += 1
                    player.mana[1] += 1
            elif train == 3:
                if gold_check(self.attack):
                    player.gold -= training_cost(self.attack)
                    self.attack += 1
                    player.attack += 1
            elif train == 4:
                if gold_check(self.defence):
                    player.gold -= training_cost(self.defence)
                    self.defence += 1
                    player.defence += 1
            elif train == 5:
                break

    def show_shop(self):
        shop_action = input_handler(
            5, "What's your business?\n",
            *show_options("Buy items", "Sell items", "Train", "Potions",
                          "Exit"))
        if shop_action == 1:
            print("Not added yet!")
        elif shop_action == 2:
            print("Not added yet!")
        elif shop_action == 3:
            self.training()
        elif shop_action == 4:
            potion_shop()


name = input("What's your name? \n")
cls()

shop = Shop()

player = Character(name)
player.stats()

while True:
    while player.health[0] > 0:
        choice = input_handler(
            5, "What would you like to do? \n",
            *show_options("Adventure",
                          f"Go to an inn (Cost: {player.inn_cost} gold)",
                          "View inventory", "Shop", "Save/Load game\n"))
        if choice == 1:
            monster = adventure()
            if monster:
                battle(monster)
                player.inn_cost = round(player.inn_cost / 1.5)
                player.stats()
        elif choice == 2:
            inn()
        elif choice == 3:
            player.show_inventory()
        elif choice == 4:
            shop.show_shop()
        elif choice == 5:
            if manage_saves():
                player = load_player()

    restart = input_handler(2, "Game Over\n",
                            *show_options("restart", "exit\n"))
    if restart == 1:
        player = Character(name)
    elif restart == 2:
        raise SystemExit
