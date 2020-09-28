import os
from colorama import Fore
from emoji import emojize


# clear screen
def cls():
    os.system("cls" if os.name == "nt" else "clear")


# pass arguments to print multiple strings in a certain color
def color_print(color, *args):
    for string in args:
        print(f"{color}{string}")
    print(f"{Fore.RESET}")


# handles all numeric inputs
def input_handler(max_input, *strings):
    if max_input <= 0:
        max_input = 1
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


# return a list of strings with index
def show_options(*strings):
    options = []
    for index, string in enumerate(strings):
        options.append(emojize(f"-{index + 1}- {string}"))
    return options


# used to print the stats of an object
def print_stats(**stats):
    stats_list = []
    for attribute, value in stats.items():
        stats_list.append(f"{attribute}: {value}")
    color_print(Fore.GREEN, "STATS:", *stats_list)
