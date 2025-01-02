import json
 
# Chemins vers les fichiers (fichier source et fichier de sortie)
input_file = 'city.list.json'          # Chemin du fichier JSON dans weather_pipeline
output_file = 'french_cities.json'     # Le fichier de sortie avec les villes françaises
 
# Ouvrir et lire le fichier JSON complet
with open(input_file, 'r', encoding='utf-8') as file:
    cities = json.load(file)
 
# Filtrer les villes françaises (country = 'FR')
french_cities = [city for city in cities if city.get('country') == 'FR']
 
# Sauvegarder les villes françaises dans un nouveau fichier JSON
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(french_cities, file, indent=4)
 
# Afficher un résumé dans le terminal
print(f"Nombre de villes françaises : {len(french_cities)}")
print(f"Les IDs des villes françaises ont été sauvegardés dans '{output_file}'")
 

