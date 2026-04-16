import pandas as pd

def load_data():
    
    #Charge les 4 fichiers CSV.
    countries = pd.read_csv("data/CountriesSD.csv", index_col=0)
    summer    = pd.read_csv("data/SummerSD.csv", index_col=0)
    winter    = pd.read_csv("data/WinterSD.csv", index_col=0)
    ol_codes  = pd.read_csv("data/olympic_codes.csv")
    #users     = pd.read_csv("data/Users.csv", index_col=0)


    print(f"Countries    : {countries.shape[0]} lignes")
    print(f"Summer       : {summer.shape[0]} lignes")
    print(f"Winter       : {winter.shape[0]} lignes")
    print(f"OlympicCodes : {ol_codes.shape[0]} lignes")
    #print(f"Users        : {users.shape[0]} lignes")


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
    
    print("Nettoyage terminé !")
    return countries, summer, winter


def merge_seasons(summer, winter, ol_codes):
    """Fusionne Summer et Winter, ajoute la colonne Season,puis comble les NaN de Country via olympic_codes."""
    # Ajout de la colonne Season
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


    print(f"Fusion terminée : {len(all_olympics)} lignes")
    print(f"NaN restants dans Country : {remaining_nan}")

    return all_olympics



def enrich_data(all_olympics):
    # Garder uniquement les vraies médailles
    medals_only = all_olympics[all_olympics["Medal"] != "No Medal"].copy()

    print(f"Total médailles : {len(medals_only)}")
    return all_olympics, medals_only