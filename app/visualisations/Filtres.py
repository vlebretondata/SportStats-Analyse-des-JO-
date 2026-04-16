import pandas as pd
from sqlalchemy import func
from app.models import Session, Medailles


def filtres_sports():
    session = Session()
    sports_list = [r[0] for r in session.query(Medailles.Sport).distinct().all()]
    session.close()
    return sports_list

def filtres_pays():
    session = Session()
    pays_list = [r[0] for r in session.query(Medailles.Country)
                 .filter(Medailles.Country.isnot(None))
                 .distinct()
                 .all()]
    session.close()
    return pays_list

def filtres_saisons():
    saisons    = ["Toutes", "Summer", "Winter"]
    return saisons

def filtres_annees():
    session = Session()
    annee_min = session.query(func.min(Medailles.Year)).scalar()
    annee_max = session.query(func.max(Medailles.Year)).scalar()
    session.close()
    return annee_min, annee_max

def filtres_annees_range():
    annee_min, annee_max = filtres_annees()
    annee_range = (annee_min, annee_max)
    return annee_range

def filtres_genres():
    genres = ["Toutes", "Men",  "Women"]
    return genres