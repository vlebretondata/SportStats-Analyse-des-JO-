import sys
sys.path.insert(0, ".")

import pandas as pd
from app.data_processing import load_data, clean_data, merge_seasons, enrich_data
from app.models import engine, init_db


def insert_all():
    init_db()

    countries, summer, winter, ol_codes = load_data() 
    
    countries, summer, winter = clean_data(countries, summer, winter)
    all_olympics = merge_seasons(summer, winter, ol_codes)

    all_olympics, medals_only = enrich_data(all_olympics)

    medals_only.to_sql("Medailles", engine, if_exists="replace", index=False)
    print(f"{len(medals_only)} médailles insérées")

    countries.to_sql("Pays", engine, if_exists="replace", index=False)
    print(f"{len(countries)} pays insérés")


if __name__ == "__main__":
    insert_all()