import random
from math import ceil, sqrt
import pickle
import os

from colorama import Fore
from emoji import emojize

from entities import Monster, Character, Equipment, materials_list, equips_list, monster_tiers, monster_tiers_names, tier_attributes
from utilities import color_print, cls, input_handler, show_options

# stats of the abilities [damage multiplier, hit chance, crit chance, mana cost]
abilities = {
    "Slash": [1, 0.9, 0.1, 0],
    "Fireball": [1.5, 0.7, 0.25, 1],
    "Shock": [0.8, 1, 0.5, 1]
}

weights = [50, 30, 20, 10, 5, 1]

attacks_list = list(abilities.keys())


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
    attack = attacker.attack * abilities.get(move)[0]
    if miss < abilities.get(move)[1]:
        damage = ceil(attack - (defender.defence / sqrt(attack)))
        if damage < 1:
            damage = 0
        # get random float between 0-1 and check for critical hit, doubles damage if true
        critical_hit = random.random()
        if critical_hit < abilities.get(move)[2]:
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
    for index, action in enumerate(abilities.keys()):
        print(f"-{index + 1}- {action}")
    print()
    while True:
        selection = input_handler((len(abilities))) - 1
        # check if player has enough mana to use
        if player.mana[0] - abilities.get(attacks_list[selection])[3] < 0:
            color_print(Fore.RED, "not enough mana!")
        else:
            break
    player.mana[0] -= abilities.get(attacks_list[selection])[3]
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
        action = input_handler(2, *show_options("Attacks", "Run"))
        if action == 1:
            damage_calc(player, attacks_list[attack_check()], combat_monster)
        elif action == 2:
            if random.choice((True, False)):
                print("You successfully fled")
                break
            print("You failed to flee")
        if combat_monster.health[0] > 0:
            damage_calc(combat_monster, attacks_list[0], player)
    if combat_monster.health[0] <= 0:
        color_print(Fore.GREEN, f"You have defeated {combat_monster.name}")
        player.xp[0] += combat_monster.xp
        player.xp_check()
        player.gold += round(
            tier_attributes.get(monster.tier)[4] * random.uniform(0.8, 1.2))
        loot(combat_monster.tier)
    elif player.health[0] < 1:
        color_print(Fore.RED, f"{combat_monster.name} has defeated you")


def save_player():
    player.shop = shop
    # open player save file and dump the current player object
    save_name = input("Save name:")
    with open(f"saves/{save_name}", "wb") as player_file:
        pickle.dump(player, player_file)
    cls()
    color_print(Fore.GREEN, "Game saved!")


def load_player():
    # load player save file and set player to the loaded object
    save_files = os.listdir("saves")
    load = input_handler(len(save_files), *show_options(*save_files)) - 1
    player_load = open(f"saves/{save_files[load]}", "rb")
    cls()
    color_print(Fore.GREEN, "Game loaded!")
    return pickle.load(player_load)


def delete_save():
    save_files = os.listdir("saves")
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

    if save_action == 2:
        return True

    if save_action == 3:
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


def training_board(**attributes):
    for attribute, value in attributes.items():
        training = value * emojize(":green_square:")
        training += (10 - len(training)) * emojize(":white_large_square:")
        print(f" {training}  - {attribute}")


def train_attribute(attribute):
    player.gold -= attribute[1]
    attribute[1] = round(attribute[1]**1.1)
    attribute[0] += 1


def gold_check(training):
    if training[0] > 9:
        print("Already max level!")
        return False

    if player.gold >= training[1]:
        return True
    print("You don't have enough gold!")
    return False


def potion_shop():
    pass


def price_equipment(equipment):
    price = 50**((materials_list.index(equipment.material) / 10) + 1)
    price = round(price * (equipment.attack + equipment.mana + equipment.attack
                           + equipment.defence))
    return price


def sell_item():
    player.print_inventory()
    select_item = input_handler(len(player.inventory), "Which item?") - 1
    sell_price = price_equipment(player.inventory[select_item])
    color_print(
        Fore.YELLOW,
        f"You sold {player.inventory[select_item].name} for {price_equipment(player.inventory[select_item])} gold"
    )
    player.gold += sell_price
    del player.inventory[select_item]


class Shop:
    def __init__(self):
        self.health = [0, 150]
        self.mana = [0, 50]
        self.attack = [0, 150]
        self.defence = [0, 150]
        self.training_attributes = None
        # emoji names :green_square:   :white_large_square:

    def training(self):
        self.training_attributes = [
            self.health, self.mana, self.attack, self.defence
        ]
        while True:
            cls()
            color_print(Fore.YELLOW, f"Gold: {player.gold}")
            training_board(
                Health=self.health[0],
                Mana=self.mana[0],
                Attack=self.attack[0],
                Defence=self.defence[0])
            train = input_handler(
                5, "What would you like to train in?\n",
                *show_options(f"Health (Cost:{self.health[1]})",
                              f"Mana (Cost:{self.mana[1]})",
                              f"Attack (Cost:{self.attack[1]})",
                              f"Defence (Cost:{self.defence[1]})", "Go back"))
            if train < 5:
                if gold_check(self.training_attributes[train - 1]):
                    train_attribute(self.training_attributes[(train - 1)])
                    player.train(train)
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
            sell_item()
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
                shop = player.shop

    restart = input_handler(2, "Game Over\n",
                            *show_options("Restart", "Exit\n"))
    if restart == 1:
        player = Character(name)
    elif restart == 2:
        print("Thanks for playing!")
        raise SystemExit
