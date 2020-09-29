import random
from math import ceil, log
from implicits import implicits
from utilities import color_print, print_stats, input_handler, show_options, cls
from colorama import Fore
from monsters import gargantuan_monsters, huge_monsters, large_monsters, medium_monsters, small_monsters, tiny_monsters

# list of monster lists by difficulty
monster_tiers = [
    tiny_monsters, small_monsters, medium_monsters, large_monsters,
    huge_monsters, gargantuan_monsters
]

monster_tiers_names = [
    "tiny_monsters", "small_monsters", "medium_monsters", "large_monsters",
    "huge_monsters", "gargantuan_monsters"
]

# [health, attack, defence, avg xp, avg gold]
tier_attributes = {
    "gargantuan_monsters": [50, 50, 10, 800, 1000],
    "huge_monsters": [30, 30, 9, 400, 550],
    "large_monsters": [25, 20, 5, 180, 250],
    "medium_monsters": [18, 15, 4, 80, 120],
    "small_monsters": [13, 8, 3, 40, 80],
    "tiny_monsters": [8, 3, 2, 20, 40]
}

# list of equippable items
equips = {
    "Sword": [0, 0, 1, 0],
    "Body Armour": [1, 0, 0, 1],
    "Helmet": [2, 0, 0, 1],
    "Ring": [0, 1, 1, 0]
}

# material multiplies the base stats of an item
materials = {
    "Iron": 1,
    "Bronze": 1.5,
    "Silver": 2,
    "Gold": 2.5,
    "Platinum": 3,
    "Diamond": 4
}

# convert dictionaries to lists to use as keys
equips_list = list(equips.keys())
materials_list = list(materials.keys())
implicits_list = list(implicits.keys())


def get_base_stats(item_type):
    base_stats = equips.get(item_type)
    return base_stats


class Entity:
    def __init__(self, name, health, attack, defence):
        self.name = name
        self.health = health
        self.attack = attack
        self.defence = defence


class Equipment(Entity):
    def __init__(self, material, equip_type):
        super().__init__((material + " " + equip_type), 0, 0, 0)
        self.type = equip_type
        self.material = material
        base_stats = [
            ceil(materials.get(material) * stat)
            for stat in (get_base_stats(equip_type))
        ]
        self.health = base_stats[0]
        self.mana = base_stats[1]
        self.attack = base_stats[2]
        self.defence = base_stats[3]
        self.mod = None
        self.mod_effect = [1, 1, 1, 1]
        self.isEquipped = False

    # Apply mod changes in stats
    def change_stats(self, operation):
        if operation:
            change = self.mod_effect
        else:
            change = [ceil(1 / effect) for effect in self.mod_effect]
        self.health = round(self.health * change[0])
        self.mana = round(self.mana * change[1])
        self.attack = round(self.attack * change[2])
        self.defence = round(self.defence * change[3])

    # remove mod from an item's stats
    def remove_mod(self):
        if self.mod:
            self.name = self.name[len(self.mod) + 1:]
        self.change_stats(False)
        self.mod = None
        self.mod_effect = [1, 1, 1, 1]

    # roll new mod on item
    def roll_mod(self):
        self.remove_mod()
        self.mod = implicits_list[random.randint(0, len(implicits_list) - 1)]
        self.mod_effect = implicits.get(self.mod)
        self.name = f"{self.mod} {self.name}"
        self.change_stats(True)

    def stats(self):
        print_stats(
            Name=self.name,
            Health=self.health,
            Mana=self.mana,
            Attack=self.attack,
            Defence=self.defence,
            Mod=self.mod_effect,
            Equipped=self.isEquipped)


class Character(Entity):
    def __init__(self, player_name):
        super.__init__(player_name, [10, 10], 3, 0)
        self.name = player_name
        self.mana = [5, 5]
        self.xp = [0, 50]
        self.level = 1
        self.gold = 0
        self.inventory = []
        self.inventory.append(Equipment("Iron", "Sword"))
        self.equipment = []
        self.inn_cost = 50
        self.shop = None

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
            self.xp[1] = int(round((log(self.level, 10) + 1) * self.xp[1], 0))
            color_print(Fore.GREEN, "You've leveled up!")
            self.level_up()
            self.xp_check()

    def print_inventory(self):
        print("INVENTORY:")
        # make list of names from inventory items before printing
        for item in self.inventory:
            print(
                f"({self.inventory.index(item) + 1}) {item.name}  ({Fore.LIGHTBLUE_EX}{item.health}, {item.mana}, {item.attack}, {item.defence}{Fore.RESET})"
            )
        print()

    def show_inventory(self):
        self.print_inventory()
        inventory_action = input_handler(
            4, "What would you like to do? \n",
            *show_options("Re-roll modifier", "Equip item", "Inspect item",
                          "Cancel\n"))
        if inventory_action < 4:
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

    def train(self, attribute):
        if attribute == 1:
            self.health[1] += 1
        elif attribute == 2:
            self.mana[1] += 1
        elif attribute == 3:
            self.attack += 1
        elif attribute == 4:
            self.defence += 1


class Monster(Entity):
    def __init__(self, tier_list, tier):
        super.__init__(
            random.choice(list(tier_list)),
            [tier_attributes.get(tier)[0],
             tier_attributes.get(tier)[0]],
            tier_attributes.get(tier)[1],
            tier_attributes.get(tier)[2])
        self.tier = tier
        self.xp = round(
            tier_attributes.get(tier)[3] * random.uniform(0.8, 1.2))

    def stats(self):
        print_stats(
            Name=self.name,
            Health=self.health,
            Attack=self.attack,
            Defence=self.defence)
