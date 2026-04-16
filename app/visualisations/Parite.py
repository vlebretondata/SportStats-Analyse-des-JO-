import pandas as pd
import plotly.express as px
from sqlalchemy import func, case
from app.models import Session, Medailles


def parite_medailles_hommes_femmes_cumule():
    session = Session()
    results = session.query(
        Medailles.Year,
        # Utilisation de case pour compter les médailles hommes et femmes
        func.sum(case((Medailles.Gender == "Men", 1), else_=0))\
            .label("total_hommes"),
        func.sum(case((Medailles.Gender == "Women", 1), else_=0))\
            .label("total_femmes"))\
        .group_by(Medailles.Year)\
        .order_by(Medailles.Year)\
        .all()
    session.close()
    df = pd.DataFrame(results, columns=["Year", "total_hommes", "total_femmes"])
    df["total_hommes"] = df["total_hommes"].cumsum()
    df["total_femmes"] = df["total_femmes"].cumsum()
    fig = px.line(
        df,
        x="Year",
        y=["total_hommes", "total_femmes"],
        color_discrete_map={"total_hommes": "#4A90D9", "total_femmes": "#FF69B4"},
        title="Parité hommes/femmes aux JO — cumulé",
        labels={"value": "Nombre de médailles", "Year": "Année", "variable": "Genre"})
    fig.update_layout(xaxis_tickangle=-45)
    return fig


def parite_medailles_hommes_femmes_parJO():
    session = Session()
    results = session.query(
        Medailles.Year,
        func.sum(case((Medailles.Gender == "Men", 1), else_=0))\
            .label("total_hommes"),
        func.sum(case((Medailles.Gender == "Women", 1), else_=0))\
            .label("total_femmes"))\
        .group_by(Medailles.Year)\
        .order_by(Medailles.Year)\
        .all()
    session.close()
    df = pd.DataFrame(results, columns=["Year", "total_hommes", "total_femmes"])
    fig = px.bar(
        df,
        x="Year",
        y=["total_hommes", "total_femmes"],
        barmode="group",
        color_discrete_map={"total_hommes": "#4A90D9", "total_femmes": "#FF69B4"},
        title="Parité hommes/femmes aux JO par année",
        labels={"value": "Nombre de médailles", "Year": "Année", "variable": "Genre"})
    fig.update_layout(xaxis_tickangle=-45)
    return fig


def top_sports_femmes():
    session = Session()
    results = session.query(
        Medailles.Sport,
        func.sum(case((Medailles.Gender == "Women", 1), else_=0))\
            .label("total_femmes"))\
            .group_by(Medailles.Sport)\
            .order_by(func.sum(case((Medailles.Gender == "Women", 1), else_=0))
        .desc())\
        .limit(10)\
        .all()
    session.close()
    df = pd.DataFrame(results, columns=["Sport", "total_femmes"])
    fig = px.bar(
        df,
        x="total_femmes",
        y="Sport",
        orientation='h',
        color="Sport",
        title="Top 10 des sports les plus médaillés pour les femmes",
        labels={"total_femmes": "Nombre de médailles", "Sport": "Sport"},
        color_discrete_sequence=["#FF69B4"])
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
    return fig


def top_sports_hommes():
    session = Session()
    results = session.query(
        Medailles.Sport,
        func.sum(case((Medailles.Gender == "Men", 1), else_=0))\
            .label("total_hommes"))\
            .group_by(Medailles.Sport)\
            .order_by(func.sum(case((Medailles.Gender == "Men", 1), else_=0))
        .desc())\
        .limit(10)\
        .all()
    session.close()
    df = pd.DataFrame(results, columns=["Sport", "total_hommes"])
    fig = px.bar(
        df,
        x="total_hommes",
        y="Sport",
        orientation='h',
        color="Sport",
        title="Top 10 des sports les plus médaillés pour les hommes",
        labels={"total_hommes": "Nombre de médailles", "Sport": "Sport"},
        color_discrete_sequence=["#4A90D9"])
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
    return fig