# Pipeline de Données Météorologiques avec Flask, MongoDB et Streamlit

## Description
Ce projet est une application de pipeline de données météorologiques qui collecte, stocke, et visualise des données météorologiques pour les villes françaises. Elle utilise Flask pour l’API, MongoDB pour le stockage, et Streamlit pour la visualisation interactive.

## Fonctionnalités
- Collecte des données météorologiques réelles et factices.
- API REST pour récupérer et mettre à jour les données météorologiques.
- Visualisation des données avec des graphiques interactifs.
- Comparaison des données entre plusieurs villes.

## Architecture
L’application suit une architecture modulaire avec les composants suivants :
- **Collecte des Données** : Données collectées via l’API OpenWeatherMap ou génération de données factices.
- **Stockage** : MongoDB pour stocker les données de manière structurée.
- **API Flask** : Fournit des points d’accès RESTful pour les données.
- **Visualisation** : Streamlit pour créer un tableau de bord interactif.

## Prérequis
- Python 3.9+
- MongoDB (local ou via Docker)
- Docker et Docker Compose (optionnel pour déploiement)
- Clé API OpenWeatherMap

## Installation

### 1. Cloner le dépôt
```bash
$ git clone <URL_DU_DEPOT>
$ cd weather_pipeline
```

### 2. Installer les dépendances
Avec pip :
```bash
$ pip install -r requirements.txt
```

### 3. Configurer MongoDB
Démarrez MongoDB localement ou avec Docker :
```bash
$ docker run -d -p 27017:27017 --name mongodb mongo
```
Vérifiez la connexion à MongoDB avec Compass ou un client CLI.

### 4. Configurer la Clé API
Ajoutez votre clé API OpenWeatherMap dans le fichier `french_weather_data.py` :
```python
api_key = "VOTRE_CLE_API"
```

### 5. Exécuter le pipeline

#### Collecte des données :
```bash
$ python french_weather_data.py
```

#### API Flask :
```bash
$ python run.py
```

#### Tableau de bord Streamlit :
```bash
$ streamlit run dashboard.py
```

### 6. Option Docker
Si vous préférez exécuter tout avec Docker :
```bash
$ docker-compose up --build
```

## Utilisation

### API Flask

#### Récupérer les données d’une ville :
```http
GET /api/v1/weather?city=Paris
```

#### Ajouter ou mettre à jour des données :
```http
POST /api/v1/weather
Body : {
  "city": "Paris",
  "temperature": 12.3,
  "humidity": 75,
  "description": "Nuageux",
  "date": "2024-12-01"
}
```

### Tableau de Bord Streamlit
Accédez au tableau de bord interactif :
```bash
http://localhost:8502
```
- Comparez les évolutions de température et d’humidité pour différentes villes.
- Visualisez les types de météo via des graphiques en camembert.



## Contributeurs
- Alex OYONO 
- Basile OYONO 
- Ernest Loic ENGOUE 
- Kaoutar CHRAIM 
- Manel OUIDDIR 

