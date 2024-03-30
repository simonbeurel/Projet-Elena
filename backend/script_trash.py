import requests
from bs4 import BeautifulSoup

url = "https://m.flashscore.fr/match/vBZjNfrI/?t=statistiques-du-match"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    text_elements = soup.find_all(text=True)
    text_list = [text.strip() for text in text_elements if text.strip()]
    for i in range(len(text_list)):
        if text_list[i] == "Aces":
            print("Aces domicile",text_list[i-1])
            print("Aces extérieur", text_list[i+1])
            break

    h3_elements = soup.find_all('h3')
    for h3 in h3_elements:
        print(h3.text)

else:
    print("La requête a échoué avec le code de statut :", response.status_code)
