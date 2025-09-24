from pymongo import MongoClient
import re

# Connexion à MongoDB (localhost:27017)
client = MongoClient("mongodb://root:example@localhost:27017/")

# Choisir la base et la collection
db = client["tennis_db"]
collection = db["joueurs"]

# Chemin du fichier contenant les données
fichier = "../backend/bdd_player_id_flashscore.txt"

# Regex pour extraire nom-prénom et ID
pattern = re.compile(r'/joueur/([a-z\-]+)/([A-Za-z0-9]+)/')

with open(fichier, "r", encoding="utf-8") as f:
    for ligne in f:
        match = pattern.search(ligne)
        if match:
            nom_prenom = match.group(1).replace("-", " ")  # ex: "swiatek-iga" → "swiatek iga"
            joueur_id = match.group(2)

            # Document à insérer
            joueur = {
                "nom_prenom": nom_prenom,
                "joueur_id": joueur_id
            }

            # Insertion (évite les doublons sur joueur_id)
            collection.update_one(
                {"joueur_id": joueur_id},
                {"$set": joueur},
                upsert=True
            )

print("Import terminé ✅")
