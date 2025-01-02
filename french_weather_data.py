import json
import requests
from datetime import datetime, timedelta
from pymongo import MongoClient
import random
 
# Configuration
input_file = 'french_cities.json'
api_url = "https://api.openweathermap.org/data/2.5/weather"
api_key = "044a4e2790940bfe953d2388ba2f6723"  # Votre clé OpenWeatherMap
 
# Connexion MongoDB
client = MongoClient("mongodb://127.0.0.1:27017")  # Local MongoDB
db = client["weather_db"]  # Nom de la base de données
collection = db["weather_data"]  # Collection pour les données météo
 
# Charger les villes françaises
with open(input_file, 'r', encoding='utf-8') as file:
    french_cities = json.load(file)
 
# Fonction pour récupérer les données météo réelles via l'API
def get_weather_data(city_id):
    params = {"id": city_id, "appid": api_key, "units": "metric"}
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur pour l'ID {city_id} : {response.status_code}")
        return None
 
# Fonction pour générer des données factices
def generate_fake_data(city_name, start_date, end_date):
    fake_data = []
    current_date = start_date
    while current_date <= end_date:
        fake_data.append({
            "city": city_name,
            "temperature": round(random.uniform(-5, 15), 1),  # Température entre -5°C et 15°C
            "humidity": random.randint(30, 90),  # Humidité entre 30% et 90%
            "description": random.choice(["Ensoleillé", "Nuageux", "Pluvieux", "Orageux", "Neigeux"]),
            "date": current_date.strftime("%Y-%m-%d")
        })
        current_date += timedelta(days=1)
    return fake_data
 
# Insérer les données dans MongoDB
for city in french_cities:
    city_id = city["id"]
    city_name = city["name"]
 
    # 1. Ajouter des données factices pour décembre
    fake_data = generate_fake_data(city_name, datetime(2024, 12, 1), datetime.now())
    collection.insert_many(fake_data)
    print(f"Données factices insérées pour {city_name} (mois de décembre).")
 
    # 2. Récupérer les données actuelles via l'API
    weather_data = get_weather_data(city_id)
    if weather_data:
        document = {
            "city": weather_data["name"],
            "temperature": weather_data["main"]["temp"],
            "humidity": weather_data["main"]["humidity"],
            "description": weather_data["weather"][0]["description"],
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        collection.insert_one(document)
        print(f"Données actuelles insérées pour {weather_data['name']}.")
 
print("Processus terminé.")