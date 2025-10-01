from time import sleep, time
import datetime

from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup

import argparse

from pymongo import MongoClient

client = MongoClient("mongodb://root:example@localhost:27017/")
db = client["tennis_db"]
collection = db["joueurs"]
collection_ladder_server = db["ladder_server"]
collection_ladder_receiver = db["ladder_receiver"]

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
    # Open and read the original file
    with open("./backend/bdd_player_id_flashscore.txt", "r") as file:
        lines = file.readlines()
        # Create a list of players
        players = []
        for line in lines:
            line = line.replace("\n", "").replace("\r", "")
            players.append(line.split('/')[2] + "-" + line.split('/')[3])
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

def retrieve_player_statsAce(player_name, player_id):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        url = f"https://www.flashscore.fr/joueur/{player_name}/{player_id}/"
        page.goto(url)

        elems = page.locator(".event__match")
        print(f"Nombre de matchs trouvés : {elems.count()}")

        id_matches = []
        number_aces_player = []
        number_aces_opponent = []
        opponent_links = []

        for i in range(elems.count()):
            id_matches.append(elems.nth(i).get_attribute("id")[4:])

        for match_id in id_matches:
            is_player_home = False

            #print(f"Match id: {match_id} // Url check: https://m.flashscore.fr/match/{match_id}/?t=stats")

            #https://www.flashscore.fr/match/tennis/anisimova-amanda-nwkutKbi/swiatek-iga-jNyZsXZe/resume/stats/0/?mid=lvMNSUfB
            
            url = f"https://m.flashscore.fr/match/{match_id}/?t=stats"
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/123 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print("ERROR GET URL")
                continue
            else:
                soup = BeautifulSoup(response.text, 'html.parser')

            div = soup.find("div", {
                "class": "wcl-row_2oCpS statisticsMobi",
                "data-testid": "wcl-statistics"
            })
            tableau = []
            if div:
                raw_text = div.get_text(separator="\n", strip=True)
                lines = raw_text.split("\n")
                for item in lines:
                    if item.isdigit():
                        tableau.append(int(item))
                    else:
                        tableau.append(item)
            else:
                print("Div non trouvée dans le HTML reçu")
                continue

            links = soup.find_all("a", class_="web-link-external")
            resultats = []
            for link in links:
                texte = link.get_text(strip=True)   
                href = link.get("href")             
                resultats.append({"texte": texte, "href": href})

            if player_id in resultats[0]['href']:
                is_player_home = True
                number_aces_player.append(tableau[0])
                number_aces_opponent.append(tableau[2])
            else:
                is_player_home = False
                number_aces_player.append(tableau[2])
                number_aces_opponent.append(tableau[0])
            
        print(number_aces_player)
        print(number_aces_opponent)

        browser.close()

    return [number_aces_player, number_aces_opponent, opponent_links]

def update_player_db_stats(nb_person_ladder=300):
   
    for player in collection.find().limit(nb_person_ladder):
        name_player = player["nom_prenom"]
        id_player = player["joueur_id"]
        print(f'[X] {name_player} [X]')
        result = retrieve_player_statsAce(name_player.replace(" ", "-"), id_player)
        collection.update_one(
            {"joueur_id": id_player},
            {"$set": {"aces_server": result[0], "aces_receiver": result[1]}},
            upsert=True
        )

    print("*** DONE ALL ***")



def get_id_from_name_mongo(nom_prenom: str) -> str | None:
    """
    Retourne l'ID du joueur à partir de son nom complet.
    Exemple: "swiatek iga" -> "jNyZsXZe"
    """
    joueur = collection.find_one({"nom_prenom": nom_prenom.lower()})
    if joueur:
        return joueur["joueur_id"]
    return None

def get_name_from_id_mongo(joueur_id: str) -> str | None:
    """
    Retourne le nom complet du joueur à partir de son ID.
    Exemple: "jNyZsXZe" -> "swiatek iga"
    """
    joueur = collection.find_one({"joueur_id": joueur_id})
    if joueur:
        return joueur["nom_prenom"]
    return None

def build_ladder_receiver(nb_person_ladder=300):
    collection_ladder_receiver.delete_many({})

    for player in collection.find().limit(nb_person_ladder):
        aces_receiver = player.get("aces_receiver", [])
        if not aces_receiver:
            continue

        avg_aces_receiver = sum(aces_receiver) / len(aces_receiver)
        collection_ladder_receiver.insert_one({
            "nom_prenom": player["nom_prenom"],
            "joueur_id": player["joueur_id"],
            "avg_aces_receiver": avg_aces_receiver,
        })

    sorted_players = list(collection_ladder_receiver.find().sort("avg_aces_receiver", -1).limit(nb_person_ladder))

    collection_ladder_receiver.delete_many({})
    for index, player in enumerate(sorted_players, start=1):
        collection_ladder_receiver.insert_one({
            "nom_prenom": player["nom_prenom"],
            "joueur_id": player["joueur_id"],
            "avg_aces_receiver": player["avg_aces_receiver"],
            "rank": index
        })

    print("Ladder receiver mis à jour et trié.")


def build_ladder_server(nb_person_ladder=300):
    collection_ladder_server.delete_many({})

    for player in collection.find().limit(nb_person_ladder):
        aces_server = player.get("aces_server", [])
        if not aces_server:
            continue

        avg_aces_server = sum(aces_server) / len(aces_server)

        collection_ladder_server.insert_one({
            "nom_prenom": player["nom_prenom"],
            "joueur_id": player["joueur_id"],
            "avg_aces_server": avg_aces_server,
        })

    sorted_players = list(collection_ladder_server.find().sort("avg_aces_server", -1).limit(nb_person_ladder))

    collection_ladder_server.delete_many({})
    for index, player in enumerate(sorted_players, start=1):
        collection_ladder_server.insert_one({
            "nom_prenom": player["nom_prenom"],
            "joueur_id": player["joueur_id"],
            "avg_aces_server": player["avg_aces_server"],
            "rank": index
        })

    print("Ladder server mis à jour et trié.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--size', type=int, help='The ladder length to build')
    args = parser.parse_args()
    update_player_db_stats(args.size)
    build_ladder_server(args.size)
    build_ladder_receiver(args.size)
    
