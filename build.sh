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

# ===== MIGRATIONS FORCÉES =====
echo "📊 Migration forcée de la base de données..."
python force_migrate.py

# ===== SUPERUTILISATEUR =====
echo "📊 Création du superutilisateur..."
python manage.py shell << END
from django.contrib.auth.models import User
try:
    User.objects.filter(username='yangoethals').delete()
    User.objects.create_superuser('yangoethals', 'yangoethals@example.com', '302001')
    print("✅ Superutilisateur créé avec succès !")
except Exception as e:
    print(f"⚠️ Erreur: {e}")
END

echo "✅ Build terminé avec succès !"
