import random
from os import system
import math
from implicits import implicits
from monsters import gargantuan_monsters, huge_monsters, large_monsters, medium_monsters, small_monsters, tiny_monsters
from colorama import Fore, Style

"""idk know if it's you ash but DONT PRESS AUTO FORMAT CAUSE IT SCREWS EVERYTHING UP PLEASE"""

tier_limits = {
	"gargantuan_monsters": [50, 10, 10],
	"huge_monsters": [30, 9, 6],
	"large_monsters": [25, 8, 5],
	"medium_monsters": [18, 6, 4],
	"small_monsters": [13, 3, 3],
	"tiny_monsters": [8, 0, 2]
}

attacks = {
	"Slash": [3, 0.9, 0.1, 0],
	"Fireball": [4, 0.7, 0.25, 1],
	"Shock": [2, 1, 0.5, 1]
}

equips = {"Sword": [0, 0, 1, 0]}

monster_tiers = [tiny_monsters, small_monsters, medium_monsters, large_monsters, huge_monsters, gargantuan_monsters]

monster_tiers_names = ["tiny_monsters", "small_monsters", "medium_monsters", "large_monsters", "huge_monsters", "gargantuan_monsters"]

implicits_list = list(implicits.keys())

attacks_list = list(attacks.keys())


# handles all inputs
def input_handler(min, max, *strings):
	for string in strings:
		print(string)
	while True:
		try:
			choice = int(input())
			if choice < min or choice > max:
				color_print(Fore.RED, f"Input must be between {min} and {max}")
			else:
				break
		except:
			color_print(Fore.RED, "Enter a number!")
	return choice


# pass arguments to print multiple strings in a certain color
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


# check if the attack selection exists or can be used
def attack_check():
	print(f"{Style.RESET_ALL}")
	for index, action in enumerate(attacks.keys()):
		print(f"-{index + 1}- {action}")
	while True:
		selection = input_handler(1, (len(attacks))) - 1
		# check if player has enough mana to use
		if player.mana[0] - attacks.get(attacks_list[selection])[3] < 0:
			color_print(Fore.RED, "not enough mana!")
		else:
			break
	player.mana[0] -= attacks.get(attacks_list[selection])[3]
	print(Style.RESET_ALL)
	return selection


def battle(combat_monster):
	print(f"You are fighting a {combat_monster.name}")
	while combat_monster.health > 0 and player.health[0] > 0:
		combat_monster.stats()
		damage_calc(player, attacks_list[attack_check()], combat_monster)
		if combat_monster.health > 0:
			damage_calc(combat_monster, attacks_list[0], player)
	if combat_monster.health < 0:
		color_print(Fore.GREEN, f"You have defeated {combat_monster.name}")
		player.xp[0] += combat_monster.xp
		player.xp_check()
		player.inventory.append(Equipment("Iron", "Sword"))
	elif player.health[0] < 0:
		color_print(Fore.RED, f"{combat_monster.name} has defeated you")


def get_base_stats(item_type):
	base_stats = equips.get(item_type)
	return base_stats

class Stats:
	def __init__(self, **stats):
		self.stats = []
		for name, value in stats.items():
			self.stats.append(f"{name}: {value}")
		color_print(Fore.GREEN, "STATS:", *self.stats)


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

	# remove mod from an item's stats
	def remove_mod(self):
		self.name = self.name[len(self.mod) + 1:]
		self.health -= self.mod_effect[0]
		self.mana -= self.mod_effect[1]
		self.attack -= self.mod_effect[2]
		self.defence -= self.mod_effect[3]
		self.mod = None
		self.mod_effect = [0, 0, 0, 0]

	# roll new mod on item
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
		self.print_stats = Stats(Name=self.name, Health=self.health, Mana=self.mana, Attack=self.attack, Defence=self.defence, Mod=self.mod_effect, Equipped=self.isEquipped)


class Character:
	def __init__(self, name):
		self.name = name
		self.health = [10, 10]
		self.mana = [5, 5]
		self.attack = 3
		self.defence = 0
		self.xp = [0, 50]
		self.level = 1
		self.inventory = []

	def stats(self):
		self.print_stats = Stats(Name=self.name, Health=self.health, Mana=self.mana, Attack=self.attack, Defence=self.defence, XP=self.xp, Level=self.level)

	# allocation of stat points
	def level_up(self):
		points = 3
		while points > 0:
			allocate = input_handler(
			1, 4, "Allocate points:\n"
			"-1- HEALTH\n"
			"-2- MANA\n"
			"-3- ATTACK\n"
			"-4- DEFENCE\n")
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
			self.xp[1] = round((math.log(self.level, 10) + 1) * self.xp[1], 0)
			color_print(Fore.GREEN, "You've leveled up!")
			self.level_up()

	def show_inventory(self):
		print("INVENTORY:")
		# make list of names from inventory items before printing
		for item in self.inventory:
			print(f"({self.inventory.index(item) + 1}) {item.name}")
		inventory_action = input_handler(
		1, 4, "What would you like to do? \n"
		"-1- Re-roll modifier\n"
		"-2- Equip item\n"
		"-3- Inspect item\n"
		"-4- Exit\n")
		# if action isn't exit, select item
		if inventory_action != 4:
			select_item = input_handler(1, len(self.inventory), "Which item?") - 1
		if inventory_action == 1:
			if self.inventory[select_item].isEquipped:
				color_print(Fore.RED, "Can't re-roll while equipped")
			else:
				self.inventory[select_item].roll_mod()
				self.inventory[select_item].stats()
				color_print(Fore.GREEN, "Mod re-rolled\n")
		elif inventory_action == 2:
			self.equip_item(self.inventory[select_item])
		elif inventory_action == 3:
			self.inventory[select_item].stats()
		elif inventory_action == 4:
			system("clear")

	# check if an item is equipped before adding/removing stats
	def equip_item(self, item):
		if item.isEquipped:
			multiplier = -1
			print(f"You have unequipped {item.name}")
		else:
			multiplier = 1
			print(f"You have equipped {item.name}")
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
		self.health = tier_limits.get(tier)[0]
		self.attack = tier_limits.get(tier)[1]
		self.defence = tier_limits.get(tier)[2]
		self.xp = random.randint(20, 40)
		

	def stats(self):
		self.print_stats = Stats(Name=self.name, Health=self.health, Attack=self.attack, Defence=self.defence)

monster = Monster(monster_tiers[1], monster_tiers_names[1])

name = input("what is your name? \n")
system("clear")

player = Character(name)
player.inventory.append(Equipment("Iron", "Sword"))
player.stats()

while True:
	while player.health[0] > 0:
		choice = input_handler(
		1, 3, "What would you like to do? \n"
		"-1- Adventure \n"
		"-2- Go to an inn \n"
		"-3- View inventory\n")
		if choice == 1:
			difficulty = input_handler(
			1, 6, "Which dungeon?\n"
			"-1- The Plains\n"
			"-2- The Forest\n"
			"-3- The Caves\n"
			"-4- The Magic Forest\n"
			"-5- The Bay\n"
			"-6- Hell\n")
			monster = Monster(monster_tiers[difficulty - 1], monster_tiers_names[difficulty - 1])
			battle(monster)
			player.stats()
		elif choice == 2:
			player.health[0] = player.health[1]
			player.mana[0] = player.mana[1]
			player.stats()
		elif choice == 3:
			player.show_inventory()

	choice = input_handler(
		1, 2, "Game Over\n"
		"-1- restart\n"
		"-2- exit\n")
	if choice == 1:
		player = Character(name)
	elif choice == 2:
		exit()
