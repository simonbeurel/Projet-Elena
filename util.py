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


def retrieve_player_statsAce(player_name, player_id):
    # player_name = rybakina-elena
    # player_id = UDzElXdm

    driver = webdriver.Firefox()

    url = f"https://www.flashscore.fr/joueur/{player_name}/{player_id}/"
    driver.get(url)

    elem = driver.find_elements(By.CLASS_NAME, "event__match")
    print(f"Nombre de matchs trouvés : {len(elem)}")

    id_matches = []
    for element in elem:
        id_matches.append(element.get_attribute("id")[4:])

    for id in id_matches:
        if id==id_matches[0]:
            print("on passe")
        else:
            driver.get(f"https://www.flashscore.fr/match/{id}/#/resume-du-match/statistiques-du-match/0")
            sleep(2)
            element_data_test_id = driver.find_elements(By.TAG_NAME, 'strong')
            print(f"Nombre d'éléments : {len(element_data_test_id)}")
            for strong_element in element_data_test_id:
                if strong_element.text == "Aces":
                    print(strong_element)

    driver.close()


