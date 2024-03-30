# Initialisation des dictionnaires pour stocker les moyennes
ladder_server = {}
ladder_receiver = {}

# Lecture du fichier logs_projecte.txt
with open('logs_last_crash.txt', 'r') as f:
    lines = f.readlines()

# Parcours des lignes et extraction des données
for i in range(0, len(lines), 5):
    name_player = lines[i].split(" ")[1]

    array_aces_1 = lines[i + 2].replace(" ", "").strip()
    array_aces_1 = eval(array_aces_1)
    if len(array_aces_1)!=0:
        average_1 = sum(array_aces_1) / len(array_aces_1)
    else:
        average_1 = 0

    array_aces_2 = lines[i + 3]
    array_aces_2 = eval(array_aces_2)
    if len(array_aces_2)!=0:
        average_2 = sum(array_aces_2) / len(array_aces_2)
    else:
        average_2 = 0

    ladder_server[name_player] = average_1
    ladder_receiver[name_player] = average_2

sorted_ladder_server = dict(sorted(ladder_server.items(), key=lambda item: item[1]))
sorted_ladder_receiver = dict(sorted(ladder_receiver.items(), key=lambda item: item[1]))

file = open("../ladders/ladder_player_receiver.txt", 'w')
iterator = 1
for key,value in sorted_ladder_receiver.items():
    file.write(f"{iterator}-{key}-{value}\n")
    iterator += 1
file.close()

file = open("../ladders/ladder_player_server.txt", 'w')
iterator = 1
for key,value in sorted_ladder_server.items():
    file.write(f"{iterator}-{key}-{value}\n")
    iterator += 1
file.close()