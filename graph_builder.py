'''
The main goal of this file is to create graph
'''
import matplotlib.pyplot as plt
import numpy as np
from util import retrieve_player_statsAce, retrieve_player_ranking_receiver_ladder, retrieve_player_id


def build_graph_aces_last_10_matches(array_aces, playername):
    moyenne = sum(array_aces) / len(array_aces)
    plt.plot(range(len(array_aces)), array_aces, marker='o', linestyle='-')
    plt.axhline(y=moyenne, color='r', linestyle='--', label=f'Moyenne: {moyenne}')
    plt.xlabel('Index')
    plt.ylabel('Valeur')
    plt.title(f"Nombre d'aces sur les 10 derniers matchs de {playername}")
    plt.legend()
    plt.show()

def build_graph_aces_against_ranked_receiver(array_aces, array_opponents, playername, nameOpponent):
    print(array_opponents)
    array_rankings_opponents = []
    for i in range(len(array_opponents)):
        result = retrieve_player_ranking_receiver_ladder(array_opponents[i])
        if result==None:
            print(f"Le joueur {array_opponents[i]} n'a pas de ranking")
        array_rankings_opponents.append(result)

    #remove every None in the array
    while None in array_rankings_opponents:
        array_rankings_opponents.remove(None)

    array_rankings_opponents.append('0')
    array_aces.append(0)

    array_rankings_opponents = [int(rank) for rank in array_rankings_opponents]

    #trier le tableau des rankings
    array_rankings_opponents, array_aces = zip(*sorted(zip(array_rankings_opponents, array_aces)))

    ranking_opponent_target = retrieve_player_ranking_receiver_ladder(nameOpponent)
    plt.plot(array_rankings_opponents, array_aces, marker='o', linestyle='-')
    plt.title(f"Nombre d'aces de {playername} en fonction du rank de l'adversaire")
    plt.xlabel("Rank de l'adversaire")
    plt.ylabel("Nombre d'aces")
    aces_value = np.interp(ranking_opponent_target, array_rankings_opponents, array_aces)

    print()
    print("Ranking de l'adversaire: ", ranking_opponent_target)
    print("Nombre d'aces attendus: ", aces_value)

    plt.show()

playerName="garcia-caroline"
id_player = "8fw1CCQC"
result = retrieve_player_statsAce(playerName,id_player)
#print(result)
#build_graph_aces_last_10_matches(result[0][::-1], playerName)
build_graph_aces_against_ranked_receiver(result[0][::-1], result[2][::-1], playerName, "Danielle Collins")