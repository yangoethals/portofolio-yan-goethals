#!/bin/bash

echo "🔨 Build du portfolio pour Render..."

# Afficher la version de Python
echo "Version Python utilisée :"
python --version

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Créer les migrations et migrer
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur par défaut
echo "from django.contrib.auth.models import User; User.objects.filter(username='yangoethals').delete(); User.objects.create_superuser('yangoethals', 'yangoethals@example.com', '302001')" | python manage.py shell || true

echo "✅ Build terminé !"
