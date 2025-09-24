# Utilisation de l'image de base Python
FROM mcr.microsoft.com/playwright/python:v1.55.0-jammy

# Mettre à jour le gestionnaire de paquets et les paquets existants
RUN apt update && apt upgrade -y

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers du projet dans le conteneur
COPY . .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt
