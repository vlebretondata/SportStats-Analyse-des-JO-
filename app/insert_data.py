# Script d'insertion des données dans la base de données et de création d'un utilisateur admin par défaut

import pandas as pd
from app.data_processing import load_data, clean_data, merge_seasons, enrich_data
from app.models import engine, init_db,User, Session
import bcrypt
import sys
# Ajouter le dossier courant au path pour pouvoir importer les modules de app
sys.path.insert(0, ".")


# Fonction principale d'insertion des données
def insert_all():
    # Initialisation de la base de données (création des tables)
    init_db()

    # Chargement, nettoyage et fusion des données
    countries, summer, winter, ol_codes = load_data() 
    
    # Nettoyage des données : suppression des doublons, comblement des NaN, conversion des types
    countries, summer, winter = clean_data(countries, summer, winter)

    # Fusion des données summer et winter, ajout de la colonne Season, comblement des NaN de Country via le Code
    all_olympics = merge_seasons(summer, winter, ol_codes)

    # Enrichissement des données : ajout de la colonne Country_full_name via le mapping Code -> Country, et création d'une table ne contenant que les médailles (en filtrant sur Medal != "No Medal")
    all_olympics, medals_only = enrich_data(all_olympics)

    # Insertion des données dans la base de données via to_sql de pandas
    medals_only.to_sql("Medailles", engine, if_exists="replace", index=False)
    # Affichage du nombre de médailles insérées pour vérification
    print(f"{len(medals_only)} lignes insérées dans la table Medailles")

    # Insertion des pays dans la table Pays
    countries.to_sql("Pays", engine, if_exists="replace", index=False)
    print(f"{len(countries)} lignes insérées dans la table Pays")


# Fonction de création d'un utilisateur admin par défaut
def create_default_admin():
    session = Session()
    
    # si l'admin n'existe pas déjà, le créer avec le mot de passe "admin123" (haché avec bcrypt)
    if not session.query(User).filter_by(username="admin").first():
        hashed = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
        new_user = User(username="admin", password=hashed.decode('utf-8'))
        session.add(new_user)
        session.commit()
        print("Admin créé!")
    else:
        print("Admin existe déjà.")
    session.close()

if __name__ == "__main__":
    insert_all()
    create_default_admin()