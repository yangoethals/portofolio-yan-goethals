import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

print("📊 Forçage des migrations...")

# Supprimer les migrations existantes (pour éviter les conflits)
print("🔄 Suppression des fichiers de migration...")
import shutil
import glob

migration_files = glob.glob('*/migrations/*.py')
for f in migration_files:
    if f != '__init__.py':
        print(f"   Suppression: {f}")
        os.remove(f)

# Créer les migrations
print("📊 Création des migrations...")
call_command('makemigrations')

# Appliquer les migrations
print("📊 Application des migrations...")
call_command('migrate')

# Vérifier les tables
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"✅ {len(tables)} tables créées")

print("✅ Migrations forcées terminées avec succès !")
