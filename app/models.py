from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# Configuration de la base de données

# Création de l'engine et de la session 
engine = create_engine("sqlite:///sportstats.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)


# Définition des modèles SQLAlchemy

# Modèle pour les médailles
class Medailles(Base):
    __tablename__ = "Medailles"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    Year       = Column(Integer)
    City       = Column(String)
    Sport      = Column(String)
    Discipline = Column(String)
    Athlete    = Column(String)
    Country    = Column(String)
    Gender     = Column(String)
    Event      = Column(String)
    Medal      = Column(String)
    Season     = Column(String)
    Points     = Column(Integer)  

# Modèle pour les pays
class Pays(Base):
    __tablename__ = "Pays"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    Country        = Column(String, nullable=False)
    Code           = Column(String, nullable=False)
    Population     = Column(Integer)
    GDP_per_Capita = Column(Float)

# Modèle pour les utilisateurs(pour les futures fonctionnalités d'authentification et de gestion des utilisateurs)
class User(Base):
    __tablename__ = "Users"

    id       = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role     = Column(String, default="user")


# Fonction pour initialiser la base de données (à appeler une seule fois)
def init_db():
    Base.metadata.create_all(engine)
    print("Base de données initialisée !")