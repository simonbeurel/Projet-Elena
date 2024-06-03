from time import sleep, time
import datetime

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import requests
from bs4 import BeautifulSoup

import argparse

driver_path = '/usr/local/bin/chromedriver'

def retrieve_player_ranking_receiver_ladder(playername):
    with open("./ladders/ladder_player_receiver.txt") as file:
        lines = file.readlines()
        for line in lines:
            if line.split('-')[1].lower() == playername.lower().split(' ')[0]:
                return line.split('-')[0]

def retrieve_player_ranking_server_ladder(playername):
    with open("./ladders/ladder_player_server.txt") as file:
        lines = file.readlines()
        for line in lines:
            if line.split('-')[1].lower() == playername.lower().split(' ')[0]:
                return line.split('-')[0]

def parsing_db():
    #Open and read the original file
    with open("./backend/bdd_player_id_flashscore.txt", "r") as file:
        lines = file.readlines()
        # Create a list of players
        players = []
        for line in lines:
            line = line.replace("\n", "").replace("\r", "")
            players.append(line.split('/')[2]+"-"+line.split('/')[3])
    return players

def retrieve_player_id_from_lastname(last_name):
    players = parsing_db()
    for player in players:
        if player.split("-")[0] == last_name:
            return player.split("-")[-1]

def retrieve_player_id(last_name, first_name):
    players = parsing_db()
    for player in players:
        name_parts = player.split("-")
        nom_de_famille = " ".join(name_parts[:-2]) if len(name_parts) > 3 else name_parts[0]
        if name_parts[-2] == first_name and nom_de_famille == last_name:
            return name_parts[-1]

def retrieve_player_fullname_from_id(player_id):
    players = parsing_db()
    for player in players:
        if player.split("-")[-1] == player_id:
            return "-".join(player.split("-")[:-1])

def retrieve_player_statsAce(player_name, player_id, driver_arg=None):
    if driver_arg is None:
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    else:
        driver = driver_arg

    url = f"https://www.flashscore.fr/joueur/{player_name}/{player_id}/"
    driver.get(url)

    elems = driver.find_elements(By.CLASS_NAME, "event__match")
    print(f"Nombre de matchs trouvés : {len(elems)}")

    id_matches = []
    number_aces_player = []
    number_aces_opponent = []
    opponent_links = []
    for elem in elems:
        id_matches.append(elem.get_attribute("id")[4:])

    for match_id in id_matches:
        is_player_home = False

        url = f"https://m.flashscore.fr/match/{match_id}/?t=statistiques-du-match"
        response = requests.get(url)
        if response.status_code != 200:
            print("ERROR GET URL")
            continue
        else:
            soup = BeautifulSoup(response.text, 'html.parser')

        h3_elements = soup.find_all('h3')
        h3 = h3_elements[0]
        array_players_current_match = h3.text.split('-')
        if player_name.split('-')[0].lower() in array_players_current_match[0].lower():
            is_player_home = True
            opponent_links.append(array_players_current_match[1].strip())
        else:
            is_player_home = False
            opponent_links.append(array_players_current_match[0].strip())

        text_elements = soup.find_all(text=True)
        text_list = [text.strip() for text in text_elements if text.strip()]
        for i in range(len(text_list)):
            if text_list[i] == "Aces":
                if is_player_home:
                    number_aces_player.append(int(text_list[i - 1]))
                    number_aces_opponent.append(int(text_list[i + 1]))
                else:
                    number_aces_player.append(int(text_list[i + 1]))
                    number_aces_opponent.append(int(text_list[i - 1]))
                break

    print(number_aces_player)
    print(number_aces_opponent)

    if driver_arg is None:
        driver.close()

    return [number_aces_player, number_aces_opponent, opponent_links]

def build_ladders_wta(nb_person_ladder=300):
    with open("./backend/bdd_player_id_flashscore.txt", 'r') as file:
        ladder_receiver = {}
        ladder_server = {}

        options = Options()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        result_temp = []

        iterator = 1
        for line in file.readlines():
            debut = time()
            name_player = line.split('/')[2]
            id_player = line.split('/')[3]
            print(f'[X] {name_player} {iterator}[X]')
            result = retrieve_player_statsAce(name_player, id_player, driver)
            result_temp.append(result)
            iterator += 1
            if iterator == nb_person_ladder: break
            print(f"Temps d'exécution : {time() - debut}")

    print(f'Taille : {len(result_temp)}')
    with open("./backend/bdd_player_id_flashscore.txt", 'r') as file:
        lines = file.readlines()
        print(len(lines))
        ladder_receiver.clear()
        ladder_server.clear()
        for i in range(len(result_temp)):
            if len(result_temp[i][0]) == 0:
                continue
            else:
                ladder_server[lines[i].split('/')[2]] = sum(result_temp[i][0]) / len(result_temp[i][0])
                ladder_receiver[lines[i].split('/')[2]] = sum(result_temp[i][1]) / len(result_temp[i][1])

    sorted_ladder_receiver = dict(sorted(ladder_receiver.items(), key=lambda item: item[1]))
    sorted_ladder_server = dict(sorted(ladder_server.items(), key=lambda item: item[1]))

    with open("./ladders/ladder_player_receiver.txt", 'w') as file:
        iterator = 1
        file.write(f"[+] Last modification: {datetime.datetime.now()} [+]\n")
        for key, value in sorted_ladder_receiver.items():
            file.write(f"{iterator}-{key}-{value}\n")
            iterator += 1

    with open("./ladders/ladder_player_server.txt", 'w') as file:
        iterator = 1
        file.write(f"[+] Last modification: {datetime.datetime.now()} [+]\n")
        for key, value in sorted_ladder_server.items():
            file.write(f"{iterator}-{key}-{value}\n")
            iterator += 1

    driver.close()

    print("*** DONE ALL ***")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--size', type=int, help='The ladder length to build')
    args = parser.parse_args()
    build_ladders_wta(args.size)
