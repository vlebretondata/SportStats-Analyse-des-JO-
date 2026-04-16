# 🏅 SportStats - Dashboard Olympique Sécurisé

## 📖 Présentation du Projet

SportStats est une application complète d'analyse de données historiques sur les Jeux Olympiques. Elle permet de visualiser la parité, les performances géopolitiques et les statistiques des athlètes à travers un dashboard interactif.

### **Fonctionnalités clés :**

- 🔐 **Sécurité :** Authentification avec hachage des mots de passe via Bcrypt et gestion de session  
- 📊 **Données :** Pipeline complet de nettoyage et d'enrichissement avec Pandas  
- 📈 **Visualisation :** Graphiques dynamiques avec Plotly et interface utilisateur Streamlit  

---

## 🛠️ Installation et Configuration

### 1. Préparation de l'environnement

Ouvrez votre terminal à la racine du projet pour configurer votre environnement :

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur Windows :
.\venv\Scripts\activate

# Sur Mac/Linux :
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

---

### 2. Variables d'environnement

Créez un fichier `.env` à la racine du projet (ce fichier est ignoré par Git) pour sécuriser vos clés :

```env
SECRET_KEY=votre_cle_secrete_de_session
FERNET_KEY=votre_cle_de_chiffrement_fernet
```

---

### 3. Initialisation de la base de données

Lancez le script pour traiter les fichiers CSV et remplir la base SQLite locale :

```bash
python app/insert_data.py
```

---

## 🚀 Utilisation

### Lancement du Dashboard

Actuellement, l'application fonctionne via une connexion directe entre le Dashboard et la base de données pour une performance optimale durant cette phase.

```bash
streamlit run app/dashboard.py
```

Le dashboard sera accessible sur :  
👉 http://localhost:8501

### 🏗️ Note sur l'architecture

Bien que la structure du projet soit compatible avec une architecture micro-services, la section API (Flask) n'est pas activée dans cette version.  
Le dashboard utilise directement l'ORM SQLAlchemy pour interroger `sportstats.db`.

---

## 📂 Structure du Projet

```
app/               # Modèles, scripts de traitement et visualisations
data/              # Sources de données brutes (CSV)
requirements.txt   # Dépendances Python
.gitignore         # Fichiers sensibles ignorés (venv, .db, .env)
```

---

## 🎓 Contexte

Projet réalisé dans le cadre de la formation **Python Dataviz & Sécurité** (Avril 2026).
