import streamlit as st
import pandas as pd    
import plotly.express as px
from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient("mongodb://mongodb:27017")
db = client["weather_db"]
collection = db["weather_data"]

# Charger les données depuis MongoDB
data = pd.DataFrame(list(collection.find()))

# Vérifier si les données sont disponibles
if data.empty:
    st.error("Aucune donnée météo disponible dans la base MongoDB.")
else:
    # Convertir les colonnes appropriées
    data["date"] = pd.to_datetime(data["date"])  # Convertir 'date' en type datetime

    # Titre principal
    st.title("Tableau de Bord Météorologique")

    # Menu multisélection pour choisir plusieurs villes
    selected_cities = st.multiselect(
        "Sélectionnez une ou plusieurs villes :", 
        options=data["city"].unique(), 
        default=data["city"].unique()[:2]  # Par défaut, afficher les deux premières villes
    )

    # Filtrer les données pour les villes sélectionnées
    filtered_data = data[data["city"].isin(selected_cities)]

    # Ajout d'une plage de dates pour filtrer
    start_date = st.date_input("Date de début", value=filtered_data["date"].min())
    end_date = st.date_input("Date de fin", value=filtered_data["date"].max())
    filtered_data = filtered_data[
        (filtered_data["date"] >= pd.to_datetime(start_date)) &
        (filtered_data["date"] <= pd.to_datetime(end_date))
    ]

    # Vérifier si des données sont disponibles après filtrage
    if filtered_data.empty:
        st.warning("Aucune donnée disponible pour les filtres sélectionnés.")
    else:
        # Agréger les données pour éviter les doublons par ville et date
        filtered_data = filtered_data.groupby(["city", "date"], as_index=False).agg({
            "temperature": "mean",  # Moyenne des températures
            "humidity": "mean",     # Moyenne de l'humidité
            "description": "first"  # Premier type de météo
        })

        # Graphique des températures
        st.subheader("Évolution des Températures (Comparaison des Villes)")
        fig_temp = px.line(
            filtered_data,
            x="date",
            y="temperature",
            color="city",
            title="Évolution des Températures",
            labels={"temperature": "Température (°C)", "date": "Date", "city": "Ville"}
        )
        st.plotly_chart(fig_temp)

        # Graphique de l'humidité
        st.subheader("Évolution de l'Humidité (Comparaison des Villes)")
        fig_humidity = px.line(
            filtered_data,
            x="date",
            y="humidity",
            color="city",
            title="Évolution de l'Humidité",
            labels={"humidity": "Humidité (%)", "date": "Date", "city": "Ville"}
        )
        st.plotly_chart(fig_humidity)

        # Ajout de camemberts pour comparer les types de météo entre deux villes
        st.subheader("Comparaison des Types de Météo (Camemberts)")
        if len(selected_cities) == 2:
            # Camembert pour la première ville
            city_1_data = filtered_data[filtered_data["city"] == selected_cities[0]]
            fig_city_1 = px.pie(
                city_1_data,
                names="description",
                title=f"Répartition des Types de Météo - {selected_cities[0]}",
                hole=0.3
            )
            st.plotly_chart(fig_city_1)

            # Camembert pour la deuxième ville
            city_2_data = filtered_data[filtered_data["city"] == selected_cities[1]]
            fig_city_2 = px.pie(
                city_2_data,
                names="description",
                title=f"Répartition des Types de Météo - {selected_cities[1]}",
                hole=0.3
            )
            st.plotly_chart(fig_city_2)
        elif len(selected_cities) < 2:
            st.warning("Veuillez sélectionner **exactement deux villes** pour comparer les types de météo.")
        else:
            st.warning("La comparaison est limitée à **deux villes à la fois**.")
