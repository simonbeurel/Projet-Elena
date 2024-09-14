# Utilisation de l'image de base Python
FROM python:3.9

# Mettre à jour le gestionnaire de paquets et les paquets existants
RUN apt update && apt upgrade -y

# Installer wget
RUN apt install -y wget

# Télécharger le paquet Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Installer Google Chrome
RUN dpkg -i google-chrome-stable_current_amd64.deb || apt -f install -y
RUN dpkg -i google-chrome-stable_current_amd64.deb

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers du projet dans le conteneur
COPY . .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install selenium
RUN pip install webdriver-manager
# Exposer le port sur lequel le serveur Flask écoute
EXPOSE 5000

# Commande pour lancer le serveur Flask
CMD ["python", "launch_server.py"]
