import pandas as pd
import plotly.express as px
from sqlalchemy import func,case    
from app.models import Session, Medailles, Pays



def afficher_carte_medailles():
    session = Session()
    # Récupération des données : nombre total de médailles par pays
    results = session.query(
        Medailles.Country,
        func.count(Medailles.Medal)\
            .label("total_medals"))\
            .filter(Medailles.Year)\
            .group_by(Medailles.Country).all()
    pays = session.query(Pays.Country, Pays.Code).all()
    session.close()
    # Création du DataFrame
    df_query = pd.DataFrame(results, columns=["Country", "total_medals"])
    df_query = df_query.sort_values(by="total_medals", ascending=False)
    # Fusion avec les codes pays pour la carte choroplèthe
    df_countries = pd.DataFrame(pays, columns=["Country", "Code"])
    df_query = df_query.merge(df_countries, on="Country", how="left")
    # Création de la carte c
    fig = px.choropleth(
        df_query,
        locations="Code",
        color="total_medals",
        hover_name="Country",
        color_continuous_scale=px.colors.sequential.YlOrRd,
        title="Nombre de médailles par pays (JO été + hiver)")
    return fig 



def graph_gdp_medals():
    session = Session()
    results = session.query(
        Pays.Country,
        Pays.GDP_per_Capita,
        Pays.Population,
        func.count(Medailles.Medal).label("Total_Medals"))\
        .join(Medailles, Medailles.Country == Pays.Country)\
        .group_by(Pays.Country, Pays.GDP_per_Capita, Pays.Population)\
        .all()  
    session.close()
    # Conversion en DataFrame
    df = pd.DataFrame(results, columns=["Country", "GDP_per_Capita", "Population", "Total_Medals"])
    #nuage de points : PIB par habitant vs nombre de médailles, avec la taille des points représentant la population
    fig = px.scatter(
        df,
        x="GDP_per_Capita",
        y="Total_Medals",
        size="Population", 
        color="Country",
        hover_name="Country",
        log_x=True, 
        title="Corrélation : PIB par habitant vs Nombre de médailles",
        labels={
            "GDP_per_Capita": "PIB par habitant (Log)",
            "Total_Medals": "Nombre total de médailles"
        },
        height=600
    )
    return fig


def graph_classement_ratio():
    session = Session()
    results = session.query(
        Pays.Country,
        Pays.Population,
        func.count(Medailles.Medal)\
        .label("Total_Medals"))\
        .join(Medailles, Medailles.Country == Pays.Country)\
        .group_by(Pays.Country, Pays.Population)\
        .all()  
    session.close()
    # Création du DataFrame
    df = pd.DataFrame(results, columns=["Country", "Population", "Total_Medals"])
    # Calcul du nombre d'habitants par médaille (plus ce ratio est bas, plus le pays est efficace)
    df = df[df["Total_Medals"] > 0]
    df["Habitants_par_Medaille"] = df["Population"] / df["Total_Medals"]
        # Tri et sélection du Top 20 (le plus petit nombre d'habitants par médaille est le meilleur)
    df_top_efficiency = df.sort_values("Habitants_par_Medaille").head(20)
    # Graphique en barres horizontales du Top 20 des pays les plus efficaces (le plus petit ratio en haut)
    fig = px.bar(
        df_top_efficiency,
        x="Habitants_par_Medaille",
        y="Country",
        orientation='h',
        title="Top 20 de l'efficacité : Nombre d'habitants par médaille",
        labels={"Habitants_par_Medaille": "Habitants pour 1 médaille"},
        color="Habitants_par_Medaille",
        color_continuous_scale="Viridis_r",
        height=600
    )
    # Pour afficher le plus efficace (plus petit ratio) en haut
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig