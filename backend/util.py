'''
The goal of this file is to define some useful functions for our DB
'''
from time import sleep, time
import datetime

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

import requests
from bs4 import BeautifulSoup

import argparse

driver_path = '/usr/local/bin/chromedriver'


def retrieve_player_ranking_receiver_ladder(playername):
    file = open("./ladders/ladder_player_receiver.txt")
    lines = file.readlines()
    for line in lines:
        if line.split('-')[1].lower() == playername.lower().split(' ')[0]:
            return line.split('-')[0]


def retrieve_player_ranking_server_ladder(playername):
    file = open("./ladders/ladder_player_server.txt")
    lines = file.readlines()
    for line in lines:
        if line.split('-')[1].lower() == playername.lower().split(' ')[0]:
            return line.split('-')[0]


def parsing_db():
    #Open and read the original file
    file = open("./backend/bdd_player_id_flashscore.txt", "r")
    lines = file.readlines()
    # Create a list of players
    players = []
    for line in lines:
        line = line.replace("\n", "").replace("\r", "")
        players.append(line.split('/')[2] + "-" + line.split('/')[3])
    file.close()
    return players


def retrieve_player_id_from_lastname(last_name):
    list = parsing_db()
    for element in list:
        if element.split("-")[0] == last_name:
            return element.split("-")[-1]


def retrieve_player_id(last_name, first_name):
    list = parsing_db()
    nom_de_famille = ""
    for element in list:
        if len(element.split('-')) > 3:
            liste_nom = element.split("-")[:-2]
            nom_de_famille = " ".join(liste_nom)
        else:
            nom_de_famille = element.split("-")[0]
        if element.split("-")[-2] == first_name and nom_de_famille == last_name:
            return element.split("-")[-1]


def retrieve_player_fullname_from_id(player_id):
    list = parsing_db()
    for element in list:
        if element.split("-")[-1] == player_id:
            #return tous les éléments suaf le dernier
            return "-".join(element.split("-")[:-1])


def retrieve_player_statsAce(player_name, player_id, driver_arg=None):
    # player_name = rybakina-elena
    # player_id = UDzElXdm

    if driver_arg is None:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        driver = driver_arg

    url = f"https://www.flashscore.fr/joueur/{player_name}/{player_id}/"
    driver.get(url)

    elem = driver.find_elements(By.CLASS_NAME, "event__match")
    print(f"Nombre de matchs trouvés : {len(elem)}")

    id_matches = []
    number_aces_player = []
    number_aces_opponent = []
    opponent_links = []
    for element in elem:
        id_matches.append(element.get_attribute("id")[4:])

    for id in id_matches:
        is_player_home = False

        url = f"https://m.flashscore.fr/match/{id}/?t=statistiques-du-match"
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
        #print(h3_elements[0])
        #print(f"Le joueur est-il à domicile ? {is_player_home}")

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
    file = open("./backend/bdd_player_id_flashscore.txt", 'r')
    ladder_receiver = {}
    ladder_server = {}

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

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
    file.close()

    print(f'Taille : {len(result_temp)}')
    file = open("./backend/bdd_player_id_flashscore.txt", 'r')
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
    file.close()

    sorted_ladder_receiver = dict(sorted(ladder_receiver.items(), key=lambda item: item[1]))
    sorted_ladder_server = dict(sorted(ladder_server.items(), key=lambda item: item[1]))

    file = open("./ladders/ladder_player_receiver.txt", 'w')
    iterator = 1
    file.write(f"[+] Last modification: {datetime.datetime.now()} [+]\n")
    for key, value in sorted_ladder_receiver.items():
        file.write(f"{iterator}-{key}-{value}\n")
        iterator += 1
    file.close()

    file = open("./ladders/ladder_player_server.txt", 'w')
    iterator = 1
    file.write(f"[+] Last modification: {datetime.datetime.now()} [+]\n")
    for key, value in sorted_ladder_server.items():
        file.write(f"{iterator}-{key}-{value}\n")
        iterator += 1
    file.close()

    driver.close()

    print("*** DONE ALL ***")


#print(retrieve_player_statsAce("kalinskaya-anna", "KGdcQnEf"))
#build_ladder_atp_receiver(200)
#print(retrieve_player_ranking_receiver_ladder("Sakkari M. (Gre)"))
#print(retrieve_player_id_from_lastname("burel"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--size', type=int, help='The ladder length to build')
    args = parser.parse_args()
    build_ladders_wta(args.size)
