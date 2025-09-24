from pymongo import MongoClient

client = MongoClient("mongodb://root:example@localhost:27017/")
db = client["tennis_db"]
collection = db["joueurs"]

for joueur in collection.find():
    print(joueur)
