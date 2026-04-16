import sys
sys.path.insert(0, ".")

from app.auth import register_user, login_user

# Créer un utilisateur admin
user, msg = register_user("admin", "admin123", role="admin")
print(msg)

# Se connecter
token = login_user("admin", "admin123")
print("Token :", token)

# Mauvais mot de passe
token_fail = login_user("admin", "mauvaismdp")
print("Mauvais mdp :", token_fail)  # → None