'''
The main goal of this file is to create graph
'''
import matplotlib.pyplot as plt
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

def build_graph_aces_against_ranked_receiver(array_aces, array_opponents, playername):
    array_rankings_opponents = []
    index_to_remove = []
    for i in range(len(array_opponents)):
        result = retrieve_player_ranking_receiver_ladder(array_opponents[i])
        if result is None:
            index_to_remove.append(i)
        else:
            array_rankings_opponents.append(result)

    for index in sorted(index_to_remove, reverse=True):
        del array_aces[index]

    print()
    print(array_aces)
    print(array_rankings_opponents)

    plt.plot(array_rankings_opponents, array_aces, marker='o', linestyle='-')
    plt.title(f"Nombre d'aces de {playername} en fonction du rankd de l'adversaire")
    plt.xlabel("Rank de l'adversaire")
    plt.ylabel("Nombre d'aces")
    plt.show()



playerName="parry-diane"
id_player = "hQQLzcNT"
#result = retrieve_player_statsAce(playerName,id_player)
#build_graph_aces_last_10_matches(result[0][::-1], playerName)
