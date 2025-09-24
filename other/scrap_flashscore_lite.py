import requests
from bs4 import BeautifulSoup

url = "https://m.flashscore.fr/match/d416PDy2/?t=stats"

# Charger la page
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/123 Safari/537.36"
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    '''XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'''
    # Chercher la div par classe ET testid
    div = soup.find("div", {
        "class": "wcl-row_2oCpS statisticsMobi",
        "data-testid": "wcl-statistics"
    })
    tableau = []
    if div:
        print("Texte trouvé :")
        raw_text = div.get_text(separator="\n", strip=True)
        lines = raw_text.split("\n")
        for item in lines:
            if item.isdigit():
                tableau.append(int(item))
            else:
                tableau.append(item)
        print(tableau)
    else:
        print("Div non trouvée dans le HTML reçu\n")
    '''XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'''

    links = soup.find_all("a", class_="web-link-external")
    resultats = []
    for link in links:
        texte = link.get_text(strip=True)   # Le texte affiché (ex: "Iatcenko P.")
        href = link.get("href")             # Le lien complet
        resultats.append({"texte": texte, "href": href})

    for elem in resultats:
        if "ADlgOFQL" in elem['href']:
            print(f"Lien: {elem['href']}")
        else:
            print(f"Texte: {elem['texte']} - Lien: {elem['href']}")
    
else:
    print("Erreur HTTP :", response.status_code)
