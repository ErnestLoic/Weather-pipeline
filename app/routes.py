from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from datetime import datetime

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Connexion locale
db = client['weather_db']  # Nom de la base de données
collection = db['weather_data']  # Nom de la collection pour les données météo

# Déclarer le blueprint
routes_app = Blueprint("routes_app", __name__)

# Route GET pour récupérer les données météo d'une ville
@routes_app.route("/api/v1/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")  # Récupère le paramètre 'city' dans l'URL
    if not city:
        return jsonify({"error": "Veuillez fournir le paramètre 'city'."}), 400

    # Rechercher les données dans MongoDB
    weather_data = list(collection.find({"city": city}, {"_id": 0}))  # Exclut l'ID MongoDB
    if not weather_data:
        return jsonify({"error": "Données météo non trouvées pour cette ville."}), 404

    return jsonify(weather_data)  # Retourne les données au format JSON

# Route POST/PUT pour ajouter ou mettre à jour des données météo
@routes_app.route("/api/v1/weather", methods=["POST", "PUT"])
def add_or_update_weather():
    data = request.get_json()  # Récupère les données JSON envoyées dans la requête
    if not data:
        return jsonify({"error": "Données JSON manquantes."}), 400

    # Vérifiez les champs requis dans les données
    required_fields = ["city", "temperature", "humidity", "description", "date"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Champ '{field}' manquant."}), 400

    # Convertir la date au format ISO (assurez-vous que "date" est une chaîne valide)
    try:
        data["date"] = datetime.strptime(data["date"], "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Format de date invalide. Utilisez 'YYYY-MM-DD'."}), 400

    # Ajouter ou mettre à jour les données dans MongoDB (par ville et date)
    collection.update_one(
        {"city": data["city"], "date": data["date"]},  # Filtre : la ville et la date
        {"$set": data},                                # Met à jour les données
        upsert=True                                    # Insère si la ville/date n'existe pas
    )

    return jsonify({
        "message": "Données ajoutées ou mises à jour avec succès.",
        "data": data
    }), 200




