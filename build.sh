#!/bin/bash

echo "🔨 Build du portfolio pour Render..."

# Afficher la version de Python
echo "Version Python : $(python --version)"

# Mettre à jour pip
echo "📦 Mise à jour de pip..."
pip install --upgrade pip

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

# Collecter les fichiers statiques
echo "📦 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# ===== MIGRATIONS =====
echo "📊 Création des migrations..."
python manage.py makemigrations || echo "⚠️ Aucune migration créée"

echo "📊 Application des migrations..."
python manage.py migrate || echo "⚠️ Erreur lors des migrations"

# ===== SUPERUTILISATEUR =====
echo "📊 Création du superutilisateur..."
python manage.py shell << END
from django.contrib.auth.models import User
try:
    User.objects.filter(username='yangoethals').delete()
    User.objects.create_superuser('yangoethals', 'yangoethals@example.com', '302001')
    print("✅ Superutilisateur créé avec succès !")
except Exception as e:
    print(f"⚠️ Erreur création superutilisateur: {e}")
END

# Vérification des tables
echo "📊 Vérification des tables..."
python manage.py shell << END
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"✅ Tables disponibles: {len(tables)}")
for table in tables:
    print(f"   - {table[0]}")
END

echo "✅ Build terminé avec succès !"
