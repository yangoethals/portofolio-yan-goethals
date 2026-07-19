#!/bin/bash

echo "🚀 Lancement du portfolio en réseau..."

# Activation de l'environnement virtuel
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Récupération de l'IP
IP=$(hostname -I | awk '{print $1}')
if [ -z "$IP" ]; then
    IP="0.0.0.0"
fi

echo ""
echo "========================================"
echo "🌐 Portfolio YAN GOETHALS"
echo "========================================"
echo "📡 Votre IP : $IP"
echo ""
echo "🌍 Accès depuis le réseau local :"
echo "   - Site client : http://$IP:8000/"
echo "   - Interface admin : http://$IP:8000/gestion/login/"
echo ""
echo "🔐 Identifiants admin :"
echo "   - Utilisateur : yangoethals"
echo "   - Mot de passe : 302001"
echo "========================================"
echo ""

# Lancer le serveur
python manage.py runserver 0.0.0.0:8000
