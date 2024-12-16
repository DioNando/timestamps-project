import streamlit as st
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import time

# Connexion à MongoDB
client = MongoClient('mongodb://root:example@mongodb:27017/?authSource=admin')  # Connexion à MongoDB
db = client['timestamp_db']
collection = db['timestamps']

# Titre et description
st.title("Données de MongoDB")
st.write("Affichage des données en temps réel avec des graphiques interactifs.")

# Configuration de la mise à jour automatique
update_interval = st.sidebar.slider("Intervalle de mise à jour (en secondes)", 1, 60, 5)

# Fonction pour récupérer et trier les données
def get_data():
    # Récupérer les données, triées par la colonne timestamp en ordre décroissant
    data = list(collection.find().sort("timestamp", -1))  # -1 pour décroissant
    for d in data:
        d.pop('_id', None)  # Supprimer l'identifiant MongoDB pour éviter des erreurs d'affichage
    return pd.DataFrame(data)

# Boucle principale avec mise à jour automatique
placeholder = st.empty()

while True:
    # Récupération des données
    df = get_data()

    with placeholder.container():
        if not df.empty:
            # Afficher les données sous forme de tableau
            st.subheader("Tableau des données (du plus récent au plus ancien)")
            st.dataframe(df)

            # Créer un layout avec des colonnes
            col1, col2 = st.columns(2)

            # Graphique en ligne temporelle
            with col1:
                st.subheader("Évolution temporelle")
                df['formatted_date'] = pd.to_datetime(df['formatted_date'])
                line_chart = px.line(df, x='formatted_date', y='timestamp', title='Évolution des timestamps')
                st.plotly_chart(line_chart)

            # Graphique circulaire
            with col2:
                st.subheader("Répartition par catégorie")
                if 'category' in df.columns:  # Vérifier si la colonne 'category' existe
                    pie_chart = px.pie(df, names='category', title='Proportion des catégories')
                    st.plotly_chart(pie_chart)
                else:
                    st.write("Pas de données de catégorie à afficher.")

            # Histogramme avancé
            st.subheader("Distribution des timestamps")
            fig, ax = plt.subplots()
            df['formatted_date'].hist(ax=ax, bins=10, color='blue', alpha=0.7)
            ax.set_title("Distribution des timestamps")
            ax.set_xlabel("Date")
            ax.set_ylabel("Fréquence")
            st.pyplot(fig)

        else:
            st.write("Aucune donnée trouvée dans MongoDB.")

    # Attendre avant de mettre à jour
    time.sleep(update_interval)
