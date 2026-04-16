import os
import bcrypt
import jwt
import datetime
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from app.models import Session, User

# ── Chargement des clés depuis .env ──────────────────────────────
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
cipher     = Fernet(os.getenv("FERNET_KEY").encode())


# ── Brique 1 : Hachage ───────────────────────────────────────────
def hash_password(password: str) -> str:
    """Hache un mot de passe avec bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(stored_hash: str, password: str) -> bool:
    """Vérifie un mot de passe contre son hash."""
    return bcrypt.checkpw(password.encode(), stored_hash.encode())


# ── Brique 2 : Chiffrement ───────────────────────────────────────
def encrypt_field(value: str) -> str:
    """Chiffre une valeur sensible (email, username...)."""
    return cipher.encrypt(value.encode()).decode()

def decrypt_field(encrypted: str) -> str:
    """Déchiffre une valeur."""
    return cipher.decrypt(encrypted.encode()).decode()


# ── Brique 3 : JWT ───────────────────────────────────────────────
def create_token(user_id: int, role: str) -> str:
    """Génère un JWT signé, valable 2 heures."""
    payload = {
        "user_id": user_id,
        "role":    role,
        "exp":     datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str) -> dict | None:
    """Vérifie et décode un JWT. Retourne None si invalide ou expiré."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


# ── Brique 4 : Gestion utilisateurs ─────────────────────────────
def register_user(username: str, password: str, role: str = "user"):
    """Inscrit un nouvel utilisateur en base."""
    session = Session()

    existing = session.query(User).filter(User.username == username).first()
    if existing:
        session.close()
        return None, "Username déjà pris"

    user = User(
        username=username,
        password=hash_password(password),
        role=role
    )

    session.add(user)
    session.commit()
    session.close()
    return user, "Inscription réussie"


def login_user(username: str, password: str) -> str | None:
    """Vérifie les identifiants et retourne un token JWT si OK."""
    session = Session()

    user = session.query(User).filter(User.username == username).first()
    session.close()

    if not user:
        return None

    if not verify_password(user.password, password):
        return None

    return create_token(user.id, user.role)