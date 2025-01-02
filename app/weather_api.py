import requests

# Votre clé API
API_KEY = "044a4e2790940bfe953d2388ba2f6723"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_by_city(city_name):
    print(f"Ville demandée : {city_name}")  # Vérifie le paramètre envoyé
    url = f"{BASE_URL}?q={city_name}&appid={API_KEY}&units=metric"
    print(f"URL appelée : {url}")  # Vérifie l'URL construite

    try:
        response = requests.get(url)
        print(f"Statut de la réponse : {response.status_code}")  # Vérifie le code de réponse
        print(f"Contenu de la réponse : {response.text}")  # Vérifie le contenu brut de la réponse

        if response.status_code == 200:
            return response.json()  # Retourne les données JSON
        else:
            return {"error": f"Erreur {response.status_code}: {response.reason}"}
    except Exception as e:
        print(f"Erreur lors de l'appel à l'API : {e}")
        return {"error": "Une erreur est survenue lors de l'appel à l'API"}

if __name__ == "__main__":
    print(get_weather_by_city("Paris"))
