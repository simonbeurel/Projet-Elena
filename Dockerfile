# Utilisation d'une image de base Python
FROM python:3.9

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers du projet dans le conteneur
COPY . .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel le serveur Flask écoute
EXPOSE 5000

# Commande pour lancer le serveur Flask
CMD ["python", "launch_server.py"]
