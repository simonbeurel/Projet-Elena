'''
The main goal of this file is to create graph
'''
import matplotlib.pyplot as plt
from util import retrieve_player_statsAce


def build_graph_aces_last_10_matches(array_aces, playername):
    # Calcul de la moyenne
    moyenne = sum(array_aces) / len(array_aces)
    # Création du graphique
    plt.plot(range(len(array_aces)), array_aces, marker='o', linestyle='-')
    plt.axhline(y=moyenne, color='r', linestyle='--', label=f'Moyenne: {moyenne}')
    plt.xlabel('Index')
    plt.ylabel('Valeur')
    plt.title(f"Nombre d'aces sur les 10 derniers matchs de {playername}")
    plt.legend()
    plt.show()

#playerName="parry-diane"
#result = retrieve_player_statsAce(playerName,"hQQLzcNT")
#build_graph_aces_last_10_matches(result[0][::-1], playerName)
