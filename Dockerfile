# Étape 1 : Utiliser une image officielle Python comme base
FROM python:3.9-slim

# Étape 2 : Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Étape 3 : Copier le fichier des dépendances dans le conteneur
COPY requirements.txt .

# Étape 4 : Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : Copier tous les fichiers de votre projet dans le conteneur
COPY . .

# Étape 6 : Exposer le port utilisé par Streamlit
EXPOSE 8501

# Étape 7 : Lancer Streamlit
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
