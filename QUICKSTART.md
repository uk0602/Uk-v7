# 🚀 Guide de Démarrage Rapide

## Installation en 3 étapes

### 1️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2️⃣ Configurer PostgreSQL

**Option A : Installation locale**

```bash
# Windows (avec PostgreSQL installé)
psql -U postgres

# Dans psql :
CREATE DATABASE crash_db;
CREATE USER crash_user WITH ENCRYPTED PASSWORD 'hayatiusman@143';
GRANT ALL PRIVILEGES ON DATABASE crash_db TO crash_user;

\c crash_db

CREATE TABLE crash_games (
    id SERIAL PRIMARY KEY,
    game_id VARCHAR(100) UNIQUE NOT NULL,
    multiplier FLOAT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    source VARCHAR(50) DEFAULT 'xbet',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_timestamp ON crash_games(timestamp);
CREATE INDEX idx_game_id ON crash_games(game_id);
```

**Option B : Docker (recommandé)**

```bash
docker run --name crash-postgres -e POSTGRES_PASSWORD=hayatiusman@143 -e POSTGRES_USER=crash_user -e POSTGRES_DB=crash_db -p 5432:5432 -d postgres:14
```

### 3️⃣ Obtenir le Token

```bash
python update_token.py
```

Suivez les instructions :
1. Ouvrez https://ma-1xbet.com/fr/games/crash
2. DevTools (F12) > Network > WS
3. Cliquez sur `crash?ref=...`
4. Copiez la Request URL complète
5. Collez-la dans le script

## 🎮 Utilisation

### Méthode 1 : Démarrage automatique

```bash
python start.py
```

Lance automatiquement :
- Le scraper en arrière-plan
- Le dashboard sur http://localhost:8051

### Méthode 2 : Démarrage manuel

**Terminal 1 : Scraper**
```bash
python app.py
```

**Terminal 2 : Dashboard**
```bash
streamlit run dashboard/realtime_app.py --server.port 8051
```

## 📊 Accéder au Dashboard

Ouvrez votre navigateur sur : **http://localhost:8051**

Vous verrez :
- 📈 Graphiques temps réel
- 🔥 Statistiques avancées
- 📋 Export des données
- 🔑 Gestion du token

## ❓ Problèmes Courants

### "Token expiré"

```bash
python update_token.py
```

### "PostgreSQL non accessible"

Vérifiez que PostgreSQL est démarré :
```bash
# Windows
services.msc # Cherchez "PostgreSQL"

# Docker
docker ps # Vérifiez que crash-postgres tourne
```

### "Pas de données dans le dashboard"

1. Vérifiez que le scraper tourne
2. Attendez 10-20 secondes
3. Rafraîchissez le dashboard

## 📝 Commandes Utiles

```bash
# Voir les logs du scraper
tail -f logs/crash_scraper.log

# Vérifier la base de données
psql -U crash_user -d crash_db -c "SELECT COUNT(*) FROM crash_games;"

# Redémarrer le scraper
# Ctrl+C puis relancer python app.py
```

---

Pour plus d'informations, consultez le [README.md](README.md) complet.
