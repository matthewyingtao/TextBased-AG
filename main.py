import random
from os import system
import math
from implicits import implicits
from monsters import gargantuan_monsters, huge_monsters, large_monsters, medium_monsters, small_monsters, tiny_monsters
from colorama import Fore, Style

tier_1 = {"Goblin": [5, 3, 1], "Slime": [10, 1, 0], "Zombie": [8, 1, 1]}

attacks = {
    "Slash": [3, 0.9, 0.1, 0],
    "Fireball": [4, 0.7, 0.25, 1],
    "Shock": [2, 1, 0.5, 1]
}

equips = {"Sword": [0, 0, 1, 0]}

implicits_list = list(implicits.keys())

attacks_list = list(attacks.keys())

monster_multiplier_limit = [0.8, 1.2]


def color_print(color, *args):
    print(f"{color}")
    for string in args:
        print(string)
    print(f"{Style.RESET_ALL}")


def damage_calc(attacker, move, defender):
    print(Fore.RED)
    # get random float between 0-1 and check for miss
    miss = random.random()
    if miss < attacks.get(move)[1]:
        damage = (attacker.attack + attacks.get(move)[0]) - defender.defence
        # get random float between 0-1 and check for critical hit, doubles damage if true
        critical_hit = random.random()
        if critical_hit < attacks.get(move)[2]:
            damage *= 2
            color_print(Fore.GREEN, "Critical Hit!")
        # calculate damage
        try:
            defender.health[0] -= damage
        except:
            defender.health -= damage
        print(
            f"{attacker.name} used {move} and dealt {damage} damage to {defender.name}"
        )
    else:
        print("Miss!")
    print(Style.RESET_ALL)


def attack_check():
    print(f"{Style.RESET_ALL}")
    for index, action in enumerate(attacks.keys()):
        print(f"-{index + 1}- {action}")
    while True:
        try:
            selection = int(input()) - 1
            if selection < 0 or selection > (len(attacks) - 1):
                color_print(Fore.RED, "that's not a valid number!")
            elif player.mana[0] - attacks.get(attacks_list[selection])[3] < 0:
                color_print(Fore.RED, "not enough mana!")
            else:
                break
        except:
            color_print(Fore.RED, "that's not a valid number!")
    print("hi2")
    player.mana[0] -= attacks.get(attacks_list[selection])[3]
    print(Style.RESET_ALL)
    return selection


def battle(combat_monster):
    print(f"You are fighting a {combat_monster.name}")
    while combat_monster.health > 0 and player.health[0] > 0:
        damage_calc(player, attacks_list[attack_check()], combat_monster)
        if combat_monster.health > 0:
            damage_calc(combat_monster, attacks_list[0], player)
    if combat_monster.health < 0:
        color_print(Fore.GREEN, f"You have defeated {combat_monster.name}")
        player.xp[0] += combat_monster.xp
        player.xp_check()
    elif player.health[0] < 0:
        color_print(Fore.RED, f"{combat_monster.name} has defeated you")


def get_base_stats(item_type):
    base_stats = equips.get(item_type)
    return base_stats


class Equipment:
    def __init__(self, material, equip_type):
        self.name = material + " " + equip_type
        base_stats = get_base_stats(equip_type)
        self.health = base_stats[0]
        self.mana = base_stats[1]
        self.attack = base_stats[2]
        self.defence = base_stats[3]
        self.mod = "None"
        self.mod_effect = [0, 0, 0, 0]
        self.isEquipped = False
        player.inventory.append(self)

    def remove_mod(self):
        self.name = self.name[len(self.mod) + 1:]
        self.health -= self.mod_effect[0]
        self.mana -= self.mod_effect[1]
        self.attack -= self.mod_effect[2]
        self.defence -= self.mod_effect[3]
        self.mod = None
        self.mod_effect = [0, 0, 0, 0]

    def roll_mod(self):
        self.remove_mod()
        self.mod = implicits_list[random.randint(0, len(implicits_list) - 1)]
        self.mod_effect = implicits.get(self.mod)
        self.name = f"{self.mod} {self.name}"
        self.health += self.mod_effect[0]
        self.mana += self.mod_effect[1]
        self.attack += self.mod_effect[2]
        self.defence += self.mod_effect[3]

    def stats(self):
        self.attributes = vars(self)
        self.attributes_keys = list(self.attributes.keys())
        self.attributes_keys.pop()
        print(f"{Fore.GREEN}STATS:")
        for attribute in self.attributes_keys:
            print(
                f"{(attribute.replace('_', ' ').upper())}: {self.attributes.get(attribute)}"
            )
        del self.attributes
        del self.attributes_keys
        print(Style.RESET_ALL)


class Character:
    def __init__(self):
        self.name = input("what is your name? \n")
        system("clear")
        self.health = [10, 10]
        self.mana = [5, 5]
        self.attack = 3
        self.defence = 0
        self.xp = [0, 50]
        self.level = 1
        self.inventory = []

    def stats(self):
        self.attributes = vars(self)
        self.attributes_keys = list(self.attributes.keys())
        self.attributes_keys.pop()
        self.attributes_keys.pop()
        print(f"{Fore.GREEN}STATS:")
        for attribute in self.attributes_keys:
            print(
                f"{(attribute.replace('_', ' ').upper())}: {self.attributes.get(attribute)}"
            )
        del self.attributes
        del self.attributes_keys
        print(Style.RESET_ALL)

    def level_up(self):
        points = 3
        while points > 0:
            allocate = int("Allocate points:\n"
                           "-1- HEALTH\n"
                           "-2- MANA\n"
                           "-3- ATTACK\n"
                           "-4- DEFENCE\n")
            if allocate == 1:
                self.health += 1
            if allocate == 2:
                self.mana += 1
            if allocate == 3:
                self.attack += 1
            if allocate == 4:
                self.defence += 1

    def xp_check(self):
        if self.xp[0] > self.xp[1]:
            self.level += 1
            self.xp[0] -= self.xp[1]
            # XP to next level follows a logarithmic curve base 10 multiplier.
            self.xp[1] = round((math.log(self.level, 10) + 1) * self.xp[1], 0)
            color_print(Fore.GREEN, "You've leveled up!")

    def show_inventory(self):
        print("INVENTORY:")
        inventory_names = []
        for item in self.inventory:
            inventory_names.append(item.name)
        print(inventory_names)
        while True:
            try:
                select_item = int(
                    input("What would you like to do? \n"
                          "-1- Re-roll modifier\n"
                          "-2- Equip item\n"
                          "-3- Exit\n"))
                if select_item == 1:
                    remove_choice = int(input("Which item?\n")) - 1
                    if self.inventory[remove_choice].isEquipped:
                        color_print(Fore.RED, "Can't re-roll while equipped")
                    else:
                        self.inventory[remove_choice].roll_mod()
                        self.inventory[remove_choice].stats()
                        color_print(Fore.GREEN, "Mod re-rolled\n")
                elif select_item == 2:
                    equip_choice = int(input("Which item\n")) - 1
                    self.equip_item(self.inventory[equip_choice])
                elif select_item == 3:
                    system("clear")
                    break
                else:
                    color_print(Fore.RED, "that's not a valid number!\n")
            except:
                color_print(Fore.RED, "that's not a valid number!\n")

    def equip_item(self, item):
        if item.isEquipped:
            self.health[1] -= item.health
            self.mana[1] -= item.mana
            self.attack -= item.attack
            self.defence -= item.defence
            item.isEquipped = False
            print(f"You have unequipped {item.name}")
        else:
            self.health[0] += item.health
            self.health[1] += item.health
            self.mana[0] += item.mana
            self.mana[1] += item.mana
            self.attack += item.attack
            self.defence += item.defence
            item.isEquipped = True
            print(f"You have equipped {item.name}")


class Monster:
    def __init__(self, tier):
        self.name = random.choice(list(tier))
        self.multiplier = round(
            random.uniform(monster_multiplier_limit[0],
                           monster_multiplier_limit[1]), 1)
        self.health = round(tier.get(self.name)[0] * self.multiplier)
        self.attack = round(tier.get(self.name)[1] * (1 / self.multiplier))
        self.defence = tier.get(self.name)[2]
        self.xp = random.randint(20, 40)


player = Character()

dog = Equipment("Iron", "Sword")
dog.roll_mod()
dog.stats()

player.stats()

while player.health[0] > 0:
    try:
        choice = int(
            input("What would you like to do? \n"
                  "-1- Adventure \n"
                  "-2- Go to an inn \n"
                  "-3- View inventory\n"))
        if choice == 1:
            monster = Monster(tier_1)
            battle(monster)
            player.stats()
        elif choice == 2:
            player.health[0] = player.health[1]
            player.mana[0] = player.mana[1]
            player.stats()
        elif choice == 3:
            player.show_inventory()
        else:
            color_print(Fore.RED, "that's not a valid number!")
    except:
        color_print(Fore.RED, "that's not a valid number!")

print("Game Over")
