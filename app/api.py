import sys
sys.path.insert(0, ".")

import pandas as pd
from flask import Flask, request, jsonify
from sqlalchemy import func
from app.models import Session, Medailles, Pays

app = Flask(__name__)


@app.route("/api/countries/medals")
def api_countries_medals():
    session = Session()
    results = session.query(
        Medailles.Country,
        func.count(Medailles.Medal).label("total_medals")
    ).group_by(Medailles.Country)\
     .order_by(func.count(Medailles.Medal).desc())\
     .all()

    pays = session.query(Pays.Country, Pays.Code).all()

    session.close()

    df_query = pd.DataFrame(results, columns=["Country", "total_medals"])
    df_countries = pd.DataFrame(pays, columns=["Country", "Code"])
    df_query = df_query.merge(df_countries, on="Country", how="left")

    result = df_query.to_dict(orient="records")
    return jsonify(result)


@app.route("/api/sports/top")
def api_top_sports():
    session = Session()

    results = session.query(
        Medailles.Sport,
        Medailles.Season,
        func.count(Medailles.Sport).label("total")
    ).group_by(Medailles.Sport, Medailles.Season)\
     .order_by(func.count(Medailles.Sport).desc())\
     .limit(20)\
     .all()

    session.close()

    df = pd.DataFrame(results, columns=["Sport", "Season", "total"])
    return jsonify(df.to_dict(orient="records"))


@app.route("/api/athletes/top")
def api_top_athletes():
    session = Session()

    results = session.query(
        Medailles.Athlete,
        Medailles.Country,
        func.count(Medailles.Medal).label("total_medals")
    ).group_by(Medailles.Athlete, Medailles.Country)\
     .order_by(func.count(Medailles.Medal).desc())\
     .limit(10)\
     .all()

    session.close()

    df = pd.DataFrame(results, columns=["Athlete", "Country", "total_medals"])
    return jsonify(df.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)



