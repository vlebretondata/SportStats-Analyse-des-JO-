import pandas as pd

def load_data():
    
    #Chargement des fichiers CSV
    countries = pd.read_csv("data/CountriesSD.csv", index_col=0)
    summer    = pd.read_csv("data/SummerSD.csv", index_col=0)
    winter    = pd.read_csv("data/WinterSD.csv", index_col=0)
    ol_codes  = pd.read_csv("data/olympic_codes.csv")
    #users     = pd.read_csv("data/Users.csv", index_col=0)

    # Vérification du nombre de lignes chargées
    print(f"Countries    : {countries.shape[0]} lignes")
    print(f"Summer       : {summer.shape[0]} lignes")
    print(f"Winter       : {winter.shape[0]} lignes")
    print(f"OlympicCodes : {ol_codes.shape[0]} lignes")
    #print(f"Users        : {users.shape[0]} lignes")

    # retourn countries, summer, winter, ol_codes, users(dans le futur)
    return countries, summer, winter, ol_codes, 


def clean_data(countries, summer, winter):

    # Supprimer les doublons
    countries = countries.drop_duplicates().copy()
    summer    = summer.drop_duplicates().copy()
    winter    = winter.drop_duplicates().copy()

    # Supprimer les lignes où Country est NaN (impossible de les récupérer via Code)
    countries = countries.dropna(subset=["Country"])
    
    # Combler les NaN de Medal par "No Medal"
    summer["Medal"] = summer["Medal"].fillna("No Medal")
    winter["Medal"] = winter["Medal"].fillna("No Medal")
    
    # Convertir Year en integer 
    summer["Year"]  = summer["Year"].astype(int)
    winter["Year"]  = winter["Year"].astype(int)

    # convertir Population en integer (après avoir comblé les NaN par 0)
    countries["Population"] = countries["Population"].fillna(0).astype(int)
    
    return countries, summer, winter


def merge_seasons(summer, winter, ol_codes):
    
    # Ajout de la colonne Season aux tables summer et winter
    summer["Season"] = "Summer"
    winter["Season"] = "Winter"

    # Fusion des deux tables
    all_olympics = pd.concat([summer, winter], ignore_index=True)

    # Création d'un dictionnaire Code -> Country depuis olympic_codes
    code_to_country = ol_codes.set_index("Code")["Nom"].to_dict()

    # Remplissage des NaN de Country via le Code
    mask = all_olympics["Country"].isna() & all_olympics["Code"].notna()
    all_olympics.loc[mask, "Country"] = all_olympics.loc[mask, "Code"].map(code_to_country)

    # Vérification
    remaining_nan = all_olympics["Country"].isna().sum()

    #vérification du nombre de lignes après fusion et du nombre de NaN restants dans Country
    print(f"Fusion terminée : {len(all_olympics)} lignes")
    print(f"NaN restants dans Country : {remaining_nan}")

    #retourne all_olympics comprenant les tables summer et winter fusionnées, avec la colonne Season et les NaN de Country comblés via le Code
    return all_olympics


def enrich_data(all_olympics):
    # Création du barème de points
    bareme = {
        "Gold": 3,
        "Silver": 2,
        "Bronze": 1
    }
    
    # Ajout de la colonne calculée
    all_olympics["Points"] = all_olympics["Medal"].map(bareme).fillna(0).astype(int)
    
    # filtre pour n'avoir que les médaillés pour l'analyse spécifique
    medals_only = all_olympics[all_olympics["Medal"] != "No Medal"].copy()

    print(f"Enrichissement terminé : Colonne 'Points' ajoutée.")
    print(f"Total médailles : {len(medals_only)}")
    
    return all_olympics, medals_only