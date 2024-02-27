'''
The goal of this file is to define some useful functions for our DB
'''

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


