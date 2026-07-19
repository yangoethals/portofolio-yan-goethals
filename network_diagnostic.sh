#!/bin/bash

echo "🔍 Diagnostic réseau..."

# Afficher toutes les IPs
echo ""
echo "📡 Adresses IP disponibles :"
ip -4 addr show | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | grep -v '127.0.0.1' | while read ip; do
    echo "   - $ip"
done

# Vérifier le port
echo ""
echo "🔍 Port 8000 :"
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null; then
    echo "   ✅ Le serveur est en cours d'exécution sur le port 8000"
    echo "   Processus : $(lsof -Pi :8000 -sTCP:LISTEN -t)"
else
    echo "   ❌ Aucun serveur en cours d'exécution sur le port 8000"
fi

# Vérifier le pare-feu
echo ""
echo "🛡️ Pare-feu :"
if command -v ufw &> /dev/null; then
    if ufw status | grep -q "Status: active"; then
        echo "   ✅ UFW est actif"
        echo "   Règles :"
        ufw status | grep 8000 || echo "   ⚠️ Aucune règle pour le port 8000"
    else
        echo "   ⚠️ UFW est inactif"
    fi
else
    echo "   ⚠️ UFW non installé"
fi

# Tester la connexion locale
echo ""
echo "🌐 Test de connexion :"
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ | grep -q "200"; then
    echo "   ✅ Le serveur répond localement"
else
    echo "   ❌ Le serveur ne répond pas localement"
fi

echo ""
echo "💡 Pour accéder depuis un autre appareil :"
echo "   1. Assurez-vous d'être sur le même réseau"
echo "   2. Utilisez l'IP affichée ci-dessus"
echo "   3. Vérifiez que le port 8000 est ouvert dans le pare-feu"
