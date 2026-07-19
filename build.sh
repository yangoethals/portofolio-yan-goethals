#!/bin/bash

echo "🔨 Build du portfolio pour Render..."

pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.filter(username='yangoethals').delete(); User.objects.create_superuser('yangoethals', 'yangoethals@example.com', '302001')" | python manage.py shell || true

echo "✅ Build terminé !"
