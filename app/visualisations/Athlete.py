import pandas as pd
import plotly.express as px
from sqlalchemy import func,case,text    
from app.models import Session, Medailles, Pays

def top_sports(filtre_saison:str = "Toutes"):
    if filtre_saison not in ["Toutes", "Summer", "Winter"]:
        return None  # ou une figure vide, ou un message d'erreur
    session = Session()

    results = session.query(
        Medailles.Sport,
        Medailles.Season,
        func.count(Medailles.Sport).label("total")
    ).group_by(Medailles.Sport, Medailles.Season)

    if filtre_saison != "Toutes":
        results = results.filter(Medailles.Season == filtre_saison)
    
    session.close()
    
    df_query = pd.DataFrame(results, columns=["Sport", "Season", "total"])
    df_query = df_query.sort_values("total", ascending=False)
 

    top_20_sports = df_query.groupby("Sport")["total"].sum().sort_values(ascending=False).head(20).index
    df_plot = df_query[df_query["Sport"].isin(top_20_sports)]

    fig = px.bar(
        df_plot,
        x="Sport",
        y="total",
        #orientation='h',
        color="Season",
        title="Top 20 des sports les plus médaillés",
        labels={"total": "Nombre de médailles", "Sport": "Sport"},
        color_discrete_map={"Summer": "#F1E31E", "Winter": "#DBDEE9"}
    )

    # Tri des barres par ordre décroissant du total (en sommant les saisons si filtre_saison == "Toutes")
    fig.update_layout(
        xaxis={'categoryorder':'total descending'},
        xaxis_tickangle=-45
    ) 

    return fig 


def top_athletes(filtre_saison:str = "Toutes"):
    session = Session()

    results = session.query(
        Medailles.Athlete,
        Medailles.Country,
        Medailles.Gender, 
        Medailles.Season,
        Medailles.Sport,
        func.count(Medailles.Medal).label("total")
    ).group_by(
        Medailles.Athlete, 
        Medailles.Country,
        Medailles.Gender,  
        Medailles.Season,
        Medailles.Sport
    ).order_by(
        func.count(Medailles.Medal).desc()
    )
    
    if filtre_saison != "Toutes":
        results = results.filter(Medailles.Season == filtre_saison)

    results = results.limit(20).all()
    
    session.close()

    df = pd.DataFrame(results, columns=["Athlete", "Country", "Genre","Sport", "Season", "total"])

    fig = px.bar(
        df,
        x="total",
        y="Athlete",
        color="Genre", 
        color_discrete_map={"Men": "#4A90D9", "Women": "#FF69B4"},
        title="Top 20 athlètes — Classement par médailles",
        labels={
            "total": "Nombre de médailles", 
            "Athlete": "Athlète",
            "Sport": "Discipline", 
            "Season": "Saison",
            "Genre": "Genre"
        },
        text="total",
        height=700,
        hover_data=["Country", "Sport", "Season"]
    )
    
    
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
       #xaxis_tickangle=-45,
        showlegend=True,
        
    )
    
    return fig 
