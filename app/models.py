from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///sportstats.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)


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


class Pays(Base):
    __tablename__ = "Pays"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    Country        = Column(String, nullable=False)
    Code           = Column(String, nullable=False)
    Population     = Column(Integer)
    GDP_per_Capita = Column(Float)

class User(Base):
    __tablename__ = "Users"

    id       = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role     = Column(String, default="user")


def init_db():
    Base.metadata.create_all(engine)
    print("Base de données initialisée !")