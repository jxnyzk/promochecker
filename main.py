from clear import clear
import shutil
import fade
import yaml
import colorama
import datetime
import os
import time
import requests
from dateutil import parser
import random
import threading
import sys
import itertools

colorama.init(autoreset=True) 

text = """
╦  ╦┌─┐┬  ┌─┐┌─┐┬┌┬┐┬ ┬  ╔═╗┬ ┬┌─┐┌─┐┬┌─┌─┐┬─┐ 
╚╗╔╝├┤ │  │ ││  │ │ └┬┘  ║  ├─┤├┤ │  ├┴┐├┤ ├┬┘ 
 ╚╝ └─┘┴─┘└─┘└─┘┴ ┴  ┴   ╚═╝┴ ┴└─┘└─┘┴ ┴└─┘┴└─ 
"""

theme_colors = {
    'black': "\x1b[38;2;75;75;77m",
    'purple': "\x1b[38;2;100;0;230m",
    'green': "\x1b[38;2;0;255;180m",
    'blue': "\x1b[38;2;5;53;230m",
    'red': "\x1b[38;2;228;71;7m",
    'pink': "\x1b[38;2;226;3;156m",
    'yellow': "\x1b[38;2;84;228;7m",
}

current_time = datetime.datetime.now().strftime("%H:%M:%S")

def logger(message):
    theme_colors = {
        'black': "\x1b[38;2;75;75;77m",
        'purple': "\x1b[38;2;100;0;230m",
        'green': "\x1b[38;2;0;255;180m",
        'blue': "\x1b[38;2;5;53;230m",
        'red': "\x1b[38;2;228;71;7m",
        'pink': "\x1b[38;2;226;3;156m",
        'yellow': "\x1b[38;2;84;228;7m",
    }

    try:
        with open('./config.yml', 'r') as file:
            config = yaml.safe_load(file)
            theme = config.get('Theme', 'black')
    except FileNotFoundError:
        theme = 'black'
    except yaml.YAMLError:
        theme = 'black'

    color = theme_colors.get(theme, theme_colors['black'])

    log_message = f"{color}[ {current_time} ]\x1b[0m >> {message}\x1b[0m"
    print(log_message)

def center_text(text):
    terminal_width = shutil.get_terminal_size().columns
    centered_text = []
    for line in text.split('\n'):
        centered_text.append(line.center(terminal_width))
    return '\n'.join(centered_text)

def create_default_config(file_path):
    os.system(f"title Velocity Checker / By: jxnyzk and usdf3lony")
    
    config_content = 'Theme: "green" # Either "black", "purple", "green", "blue", "red", "pink", "yellow"\n'

    with open(file_path, 'w') as file:
        file.write(config_content)
    
    faded_text = fade.pinkred(text)
    print(center_text(faded_text))


    custom_text1 = "\x1b[38;2;226;3;156mjxnyzk"
    custom_text2 = "\x1b[38;2;226;3;156musdf3lony"
    custom_color1 = "\x1b[38;2;226;3;156m"
    custom_color2 = "\x1b[37m"
    print(center_text("                   Made by: " + custom_text1 + "\x1b[37m and " + custom_text2))
    print(center_text(""))
    print(f"{custom_color1}[ {current_time} ] >>{custom_color2} Config.yml file got created.")
    print(f"{custom_color1}[ {current_time} ] >>{custom_color2} Please restart, and fill in the config.yml file!")
    return True

def read_config(file_path):
    file_path = './config.yml'
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def create_folders():
    folders = ['Output', 'Data']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
    
    files = ['proxies.txt', 'promos.txt']
    data_folder_path = 'Data'
    for file in files:
        file_path = os.path.join(data_folder_path, file)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write('')
    
    files2 = ['invalid.txt', 'valid.txt', 'redeemed.txt', 'ratelimited.txt']
    Output_folder_path = 'Output'
    for file in files2:
        file_path = os.path.join(Output_folder_path, file)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write('')

config_file_path = './config.yml'
config = read_config(config_file_path)
theme = config.get('Theme', '').lower()

def load_gift_codes():
    with open('./Data/promos.txt', 'r') as file:
        return [line.strip().split('https://promos.discord.gg/')[-1] for line in file if line.strip().startswith('https://promos.discord.gg/')]

def load_proxies():
    with open('./Data/proxies.txt', 'r') as file:
        return [line.strip() for line in file]

def fetch_gift_code_details():
    gift_codes = load_gift_codes()
    proxies = load_proxies() if not config.get('Proxyless', False) else []
    checked_codes_count = 0
    invalid = 0
    valid = 0 
    claimed = 0
    ratelimited = 0

    for code in gift_codes:

        anonymized_code = '-'.join(code.split('-')[:2] + ['****'])
        url = f"https://canary.discord.com/api/v10/entitlements/gift-codes/{code}"
        proxy_dict = {}

        if proxies:
            proxy = random.choice(proxies)
            proxy_dict = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
        try:
            response = requests.get(url, proxies=proxy_dict)
            if response.status_code == 200:
                data = response.json()
                expires_at = data.get('expires_at', 'Does not')
                if expires_at != 'Does not':
                    expires_at = parser.parse(expires_at).strftime('%d.%m.%y')
                redeemed = data.get('redeemed', False)
                redeemed_status = "True" if redeemed else "False"
                logger(f"Checked Gift: {anonymized_code}, Status: \x1b[38;2;0;255;180mVALID\x1b[37m, Expires on {expires_at}, Redeemed: {redeemed_status}")
                checked_codes_count += 1
                if redeemed:
                    claimed += 1
                if not redeemed:
                    valid += 1
                    with open('./Output/invalid.txt', 'a') as file:
                        file.write(f"https://promos.discord.gg/{code}\n") 
            elif response.status_code == 404:
                with open('./Output/invalid.txt', 'a') as file:
                    file.write(f"https://promos.discord.gg/{code}\n")
                logger(f"Checked Gift: {anonymized_code}, Status: \x1b[38;2;228;71;7mINVALID\x1b[37m, Response: {data}")
                invalid += 1
            elif response.status_code == 429:
                with open('./Output/ratelimited.txt', 'a') as file:
                    file.write(f"https://promos.discord.gg/{code}\n")
                logger(f"Checked Gift: {anonymized_code}, Status: \x1b[38;2;228;71;7mRATELIMITED\x1b[37m")
                ratelimited += 1
            else:
                logger(f"Failed to fetch gift code {anonymized_code}. Status Code: {response.status_code}")

            os.system(f"title Velocity Checker / Valid: {valid} / Invalid: {invalid}")

        except requests.exceptions.RequestException as e:
            logger(f"Error fetching gift code details for {anonymized_code} {e}")

    return checked_codes_count, claimed, valid, invalid, ratelimited

def main():
    os.system(f"title Velocity Checker / By: jxnyzk and usdf3lony")
    create_folders()

    fade_functions = {
        'black': fade.blackwhite,
        'purple': fade.purplepink,
        'green': fade.greenblue,
        'blue': fade.water,
        'red': fade.fire,
        'pink': fade.pinkred,
        'yellow': fade.brazil
    }

    if theme in fade_functions:
        faded_text = fade_functions[theme](text)
    else:
        faded_text = fade.blackwhite(text)

    print(center_text(faded_text))

    theme_ansi_colors = {
        'black': "\x1b[38;2;75;75;77m",
        'purple': "\x1b[38;2;100;0;230m",
        'green': "\x1b[38;2;0;255;180m",
        'blue': "\x1b[38;2;5;53;230m",
        'red': "\x1b[38;2;228;71;7m",
        'pink': "\x1b[38;2;226;3;156m",
        'yellow': "\x1b[38;2;84;228;7m",
    }
    ansi_color = theme_ansi_colors.get(theme, "\x1b[37m")
    custom_text1 = "jxnyzk"
    custom_text2 = "usdf3lony"
    print(center_text("                   Made by: " + ansi_color + custom_text1 + "\x1b[37m and " + ansi_color + custom_text2))
    print("")

    input(f"{ansi_color}[ {current_time} ] \x1b[37m>> Press Enter to start...")
    response = input(f"{ansi_color}[ {current_time} ] \x1b[37m>> Remove duplicates? (y/n): ")
    if response.lower() == 'y':
        remove_duplicates()
        input(f"{ansi_color}[ {current_time} ]\x1b[37m >> Press Enter to check!")

    checked_codes_count, claimed, valid, invalid, ratelimited = fetch_gift_code_details()
    print("")
    logger(f"Total codes checked: {checked_codes_count} >> \x1b[38;2;0;255;180mValid:\x1b[37m {valid} | \x1b[38;2;228;71;7mInvalid:\x1b[37m {invalid} | Claimed: {claimed} | \x1b[38;2;228;71;7mratelimited:\x1b[37m {ratelimited}")
    input(f"{ansi_color}[ {current_time} ] \x1b[37m>> Press Enter to exit...")

def loading_animation(stop_event):
    ansi_color = theme_colors.get(theme, "\x1b[37m")
    animation_chars = itertools.cycle(r'\|/-')
    while not stop_event.is_set():
        char = next(animation_chars)
        status = f"{ansi_color}[ {current_time} ] [{char}] \x1b[37m >> Removing... "
        sys.stdout.write(status)
        sys.stdout.flush()
        sys.stdout.write('\b' * len(status))
        time.sleep(0.2)
    sys.stdout.write('\r' + ' ' * len(status) + '\r')
    sys.stdout.flush()

def remove_duplicates():
    ansi_color = theme_colors.get(theme, "\x1b[37m")
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
    loading_thread.start()

    time.sleep(3)
    stop_event.set()

    with open("./Data/promos.txt", "r") as file:
        lines = file.read().splitlines()
    unique_lines = set(lines)

    with open("./Data/promos.txt", "w") as file:
        for line in unique_lines:
            if line:
                file.write(f"{line}\n")

    loading_thread.join()

    print(f"{ansi_color}[ {current_time} ]{ansi_color} \x1b[37m>> Removal Complete!")
    print("")

if __name__ == '__main__':
    clear()
    config_file_path = './config.yml'
    try:
        if not os.path.exists(config_file_path):
            create_default_config(config_file_path)
            time.sleep(2)
            exit()
        main()
    except KeyboardInterrupt:
        logger("Exciting...")
        time.sleep(2)
        exit()