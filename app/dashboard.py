# ── Imports ───────────────────────────────────────────────────────

import streamlit as st
from app.auth import login_user
import pandas as pd
from sqlalchemy import func, case
from app.models import Session, Medailles, Pays
from app.visualisations.KPI import (
    kpi_jo_summer,
    kpi_jo_winter,
    kpi_femmes_medaillees,
    kpi_hommes_medailles,
    kpi_total_pays,
    kpi_total_sports)
from app.visualisations.Parite import (
    parite_medailles_hommes_femmes_parJO, 
    parite_medailles_hommes_femmes_cumule,
    top_sports_femmes,
    top_sports_hommes)
from app.visualisations.Géopolitique import (
    afficher_carte_medailles,
    graph_gdp_medals,
    graph_classement_ratio)
from app.visualisations.Filtres import (
    filtres_sports,
    filtres_pays, 
    filtres_saisons, 
    filtres_annees_range, 
    filtres_genres)
from app.visualisations.Athlete import( 
    top_sports, 
    top_athletes)




# ── Configuration de la page ──────────────────────────────────────
    # On configure le titre, l'icône et la mise en page de notre dashboard Streamlit
st.set_page_config(
    page_title="Analyse des JO - SportStats",
    page_icon="🏅",
    layout="wide"
) 
# ── Authentification ─────────────────────────────────────────────

    # On utilise une session Streamlit pour stocker l'état d'authentification de l'utilisateur
# Si l'utilisateur n'est pas authentifié, affichage du formulaire de connexion
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
# Tant que l'utilisateur n'est pas authentifié, affichage du formulaire de connexion
if not st.session_state.authenticated:
    st.title("🔐 Accès sécurisé - SportStats")
    
    # Création d'un formulaire pour regrouper les champs
    with st.form("login_form"):
        username = st.text_input("Nom d'athlète (Utilisateur)")
        password = st.text_input("Mot de passe", type="password")
        submit = st.form_submit_button("Entrer sur le terrain")
        
        if submit:
            # On vérifie avec la fonction de auth.py qui retourne un token JWT si les identifiants sont corrects
            token = login_user(username, password)
            
            if token: # Si le token existe, la connexion est valide
                st.session_state.authenticated = True
                st.rerun() # On recharge la page pour passer le blocage !
            else:
                st.error("Identifiants incorrects")
                
    st.stop() # on arrete l'exécution du reste du code tant que l'utilisateur n'est pas authentifié



# ── Dashboard principal ───────────────────────────────────────────
st.title("🏅 Analyse des JO - SportStats")


# ── KPIs ──────────────────────────────────────────────────────────
    # affichege des 6 KPIs une ligne de 6 colonnes
col1, col2, col3,col4,col5,col6 = st.columns(6)

col1.metric("🌍 Pays représentés", kpi_total_pays())
col2.metric("🏊 Sports différents", kpi_total_sports())
col3.metric("☀️ JO d'été", kpi_jo_summer())
col4.metric("❄️ JO d'hiver", kpi_jo_winter())
col5.metric("👩 Femmes médaillées", kpi_femmes_medaillees())
col6.metric("👨 Hommes médaillés", kpi_hommes_medailles())

    # ligne de séparation
st.divider()

# ── Filtres sidebar ───────────────────────────────────────────────
    # création d'une barre latérale pour les filtres
st.sidebar.header("Filtres")
    # récupere les filtres contenus dans visualisations/Filtres.py et les affiche dans la sidebar
saison_filtre = st.sidebar.selectbox("Saison", filtres_saisons())
sport_filtre = st.sidebar.selectbox("Sport", ["Tous"] + sorted(filtres_sports()))
bornes = filtres_annees_range()
annee_range   = annee_range = st.sidebar.slider(    "Années",
    min_value=int(bornes[0]),    
    max_value=int(bornes[1]),    
    value=(int(bornes[0]), int(bornes[1])))
genre= st.sidebar.selectbox("Genre", filtres_genres())
pays=st.sidebar.selectbox("Pays", ["Tous"] + sorted(filtres_pays()))

    # bouton de déconnexion
if st.sidebar.button("Se déconnecter"):
    st.session_state.authenticated = False
    st.rerun()

# ── Onglets ───────────────────────────────────────────────────────
    # création de 3 onglets
tab1, tab2, tab3 = st.tabs([ "🏆 Sports et athlètes", "👩👨 Parité","🗺️ Géopolitique"])

# 1er onglet : top sports et top athlètes
with tab1:
    
    # Top sports
    st.subheader("Top 20 des sports les plus médaillés")
    fig2 = top_sports(saison_filtre)
    st.plotly_chart(fig2, width='stretch')

    # Top athlètes
    st.subheader("Top 20 des athlètes les plus médaillés")
    fig = top_athletes(saison_filtre)
    st.plotly_chart(fig, width='stretch')

#2ème onglet : parité hommes/femmes
with tab2:
    # Parité hommes/femmes cumulé à travers les années
    st.subheader("Parité hommes/femmes (cumulé) à travers les années")
    fig = parite_medailles_hommes_femmes_cumule()
    st.plotly_chart(fig, width='stretch')
    
    # Parité hommes/femmes par JO
    st.subheader("parité hommes/femmes (par JO)")
    fig = parite_medailles_hommes_femmes_parJO()
    st.plotly_chart(fig, width='stretch')
    
    # Ajout de 2 colonnes pour Top sports femmes vs hommes
    col1, col2 = st.columns(2)
    
    #top sports femmes
    with col1:
        st.subheader("Top 10 des sports les plus médaillés par les femmes")
        fig = top_sports_femmes()
        st.plotly_chart(fig, width='stretch')
    
    #top sports hommes
    with col2:
        st.subheader("Top 10 des sports les plus médaillés par les hommes")
        fig = top_sports_hommes()
        st.plotly_chart(fig, width='stretch')
    
# 3ème onglet : géopolitique des médailles   
with tab3:
    # Affichage de la carte des médailles
    st.subheader("Géopolitique des médailles")
    fig = afficher_carte_medailles(annee_range)
    st.plotly_chart(fig, width='stretch')
    
    # Graphique PIB par habitant vs nombre de médailles
    st.subheader("PIB par habitant vs Nombre de médailles")
    fig = graph_gdp_medals()
    st.plotly_chart(fig, width='stretch')

    # Graphique classement par ratio habitants/medailles
    st.subheader("Ratio médailles/population")
    fig = graph_classement_ratio()
    st.plotly_chart(fig, width='stretch')
