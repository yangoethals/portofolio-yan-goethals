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
python manage.py makemigrations

echo "📊 Application des migrations..."
python manage.py migrate

# ===== SUPERUTILISATEUR =====
echo "📊 Création du superutilisateur..."
python manage.py shell << END
from django.contrib.auth.models import User
from django.db import connection

# Vérifier si la table core_profile existe
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_profile'")
table_exists = cursor.fetchone()

if not table_exists:
    print("⚠️ La table core_profile n'existe pas. Création en cours...")
    # Les migrations devraient la créer

# Créer le superutilisateur
User.objects.filter(username='yangoethals').delete()
User.objects.create_superuser('yangoethals', 'yangoethals@example.com', '302001')
print("✅ Superutilisateur créé avec succès !")
END

echo "✅ Build terminé avec succès !"
