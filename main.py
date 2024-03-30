#!/usr/bin/env python3
import signal
from simple_term_menu import TerminalMenu
from salary.request_info import which_profession_pays_my_bills, get_salary, search_profession_by_tags
from util_functions import _get_all_jobs_as_dfs

logo = r'''
Welcome to:

/ $$$$$$$           /$$$$$$$                   
| $$__  $$         | $$__  $$                  
| $$  \ $$/$$   /$$| $$  \ $$/$$$$$$  /$$   /$$
| $$$$$$$/ $$  | $$| $$$$$$$/____  $$| $$  | $$
| $$____/| $$  | $$| $$____/ /$$$$$$$| $$  | $$
| $$     | $$  | $$| $$     /$$__  $$| $$  | $$
| $$     |  $$$$$$$| $$    |  $$$$$$$|  $$$$$$$
|__/      \____  $$|__/     \_______/ \____  $$
          /$$  | $$                   /$$  | $$
         |  $$$$$$/                  |  $$$$$$/
          \______/                    \______/
          
                  Everything you need to know about Hi-tech jobs and money
'''


def goodbye():
    exit("\nGoodbye 👋")


def signal_handler(signal, frame):
    goodbye()


function_list: list = [
    ("Get profession salary info", get_salary),
    ("Search profession by salary", which_profession_pays_my_bills),
    ("Search Possiotion by category", search_profession_by_tags),
    ("Exit", goodbye)
]


def _create_options_menu():
    menu_options = []
    for index, entry in enumerate(function_list):
        menu_options.append(f"[{index + 1}] {'' + entry[0]}")
    return menu_options


def show_main_menu() -> int:
    options = _create_options_menu()
    terminal_menu = TerminalMenu(options, title="\nYou can:")
    menu_entry_index = terminal_menu.show()
    return menu_entry_index


def start(dfs: list):
    try:
        selection = show_main_menu()
        if function_list[selection][0] != "Exit":
            function_list[selection][1](dfs)
        else:
            function_list[selection][1]()

    except Exception as e:
        print(f"Oh No! Something went wrong: {e}")


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    print(logo)
    dfs = _get_all_jobs_as_dfs()
    start(dfs)
