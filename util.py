'''
The goal of this file is to define some useful functions for our DB
'''
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver_path = '/usr/local/bin/chromedriver'



def parsing_db():
    #Open and read the original file
    file = open("bdd_player_id_flashscore.txt", "r")
    lines = file.readlines()
    # Create a list of players
    players = []
    for line in lines:
        line = line.replace("\n", "").replace("\r", "")
        players.append(line.split('/')[2]+"-"+line.split('/')[3])
    file.close()
    return players



def retrieve_player_id(first_name, last_name):
    list = parsing_db()
    nom_de_famille = ""
    for element in list:
        if len(element.split('-')) > 3:
            liste_nom = element.split("-")[:-2]
            nom_de_famille = " ".join(liste_nom)
        else:
            nom_de_famille = element.split("-")[0]
        if element.split("-")[-2]==first_name and nom_de_famille==last_name:
            return element.split("-")[-1]


def retrieve_player_statsAce(player_name, player_id, driver_arg=None):
    # player_name = rybakina-elena
    # player_id = UDzElXdm

    if driver_arg is None:
        driver = webdriver.Firefox()
    else:
        driver = driver_arg

    url = f"https://www.flashscore.fr/joueur/{player_name}/{player_id}/"
    driver.get(url)

    elem = driver.find_elements(By.CLASS_NAME, "event__match")
    print(f"Nombre de matchs trouvés : {len(elem)}")

    id_matches = []
    number_aces_player = []
    number_aces_opponent = []
    for element in elem:
        id_matches.append(element.get_attribute("id")[4:])

    for id in id_matches:
        driver.get(f"https://www.flashscore.fr/match/{id}/#/resume-du-match/statistiques-du-match/0")
        sleep(3)

        element_data_test_id = driver.find_elements(By.TAG_NAME, 'strong')

        away_home_participant = driver.find_elements(By.CLASS_NAME, "participant__participantLink")

        is_player_home = False

        if away_home_participant[0].get_attribute('href') == url:
            is_player_home = True

        for i in range(len(element_data_test_id)):
            if element_data_test_id[i].text == "Aces":
                if is_player_home:
                    number_aces_player.append(int(element_data_test_id[i - 1].text))
                    number_aces_opponent.append(int(element_data_test_id[i + 1].text))
                else:
                    number_aces_player.append(int(element_data_test_id[i + 1].text))
                    number_aces_opponent.append(int(element_data_test_id[i - 1].text))

    print(number_aces_player)
    print(number_aces_opponent)

    driver.close()

    return [number_aces_player,number_aces_opponent]


def build_ladder_atp_receiver():
    file = open("./bdd_player_id_flashscore.txt", 'r')
    ladder = {}
    for line in file.readlines():
        name_player = line.split('/')[2]
        id_player = line.split('/')[3]
        result = retrieve_player_statsAce(name_player, id_player)
        ladder[name_player] = sum(result[1]) / len(result[1])
        print(ladder)
    file.close()

    sorted_ladder = dict(sorted(ladder.items(), key=lambda item: item[1]))
    file = open("./ladder_player", 'w')

    iterator = 1
    for key,value in sorted_ladder:
        file.write(f"{iterator}-{key}-{value}\n")
        iterator += 1

    file.close()

retrieve_player_statsAce("rybakina-elena", "UDzElXdm")
#build_ladder_atp_receiver()
