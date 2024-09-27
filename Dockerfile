# Utiliser une image de base avec Python préinstallé
FROM mcr.microsoft.com/devcontainers/python:3.12

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH="/workspace/TheFarmerWasReplaceFR"

# Créer et définir le répertoire de travail
WORKDIR /workspace/TheFarmerWasReplaceFR

# INSTALL PLAYWRIGHT
RUN pip install --upgrade pip

# Copier les fichiers de l'application dans le conteneur
COPY . .

RUN git config --global --add safe.directory /workspaces/TheFarmerWasReplaceFR
RUN pip install -r requirements.txt