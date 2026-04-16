from sqlalchemy import func
from app.models import Session, Medailles, Pays

def kpi_jo_summer():
    session = Session()
    total = session.query(Medailles.Year)\
            .filter(Medailles.Season == "Summer")\
            .distinct().count()
    session.close()
    return total

def kpi_jo_winter():
    session = Session()
    total = session.query(Medailles.Year)\
            .filter(Medailles.Season == "Winter")\
            .distinct().count()
    session.close()
    return total

def kpi_femmes_medaillees():
    session = Session()
    total = session.query(Medailles.Athlete)\
            .filter(Medailles.Gender == "Women")\
            .distinct().count()
    session.close()
    return total

def kpi_hommes_medailles():
    session = Session()
    total = session.query(Medailles.Athlete)\
            .filter(Medailles.Gender == "Men")\
            .distinct().count()
    session.close()
    return total

def kpi_total_pays():
    session= Session()
    total_pays      = session.query(func.count(Pays.Country)).scalar()
    session.close()
    return total_pays

def kpi_total_sports():
    session= Session()
    total_sports    = session.query(Medailles.Sport).distinct().count()
    session.close()
    return total_sports
