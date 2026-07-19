from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    title = models.CharField(max_length=200, default="Network & System Engineer")
    bio = models.TextField(max_length=1000, default="Spécialiste en réseau et systèmes avec expertise en Python, Django et IoT.")
    location = models.CharField(max_length=100, default="France")
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profil de {self.user.username}"

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('language', 'Langage'),
        ('framework', 'Framework'),
        ('database', 'Base de données'),
        ('tool', 'Outil'),
        ('iot', 'IoT'),
        ('cloud', 'Cloud'),
        ('network', 'Réseau'),
        ('other', 'Autre'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="Nom de l'icône Font Awesome", blank=True)
    level = models.IntegerField(default=80, help_text="Niveau de compétence (1-100)")
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.get_category_display()} - {self.name}"

class NetworkSkill(models.Model):
    """Compétences réseau avancées"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    level = models.IntegerField(default=80)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class CyberSecuritySkill(models.Model):
    """Compétences cybersécurité"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    level = models.IntegerField(default=80)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class AISkill(models.Model):
    """Compétences IA/ML/DL"""
    CATEGORY_CHOICES = [
        ('ml', 'Machine Learning'),
        ('dl', 'Deep Learning'),
        ('rl', 'Reinforcement Learning'),
        ('tl', 'Transfer Learning'),
        ('agent', 'IA Agent'),
        ('other', 'Autre'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    level = models.IntegerField(default=80)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.get_category_display()} - {self.name}"

class DevOpsSkill(models.Model):
    """Compétences DevOps"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    level = models.IntegerField(default=80)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class Experience(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} chez {self.company}"

class Education(models.Model):
    school = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.degree} - {self.school}"

class Certificate(models.Model):
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    date = models.DateField()
    credential_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='certificates/', null=True, blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=[
        ('microsoft', 'Microsoft Learn'),
        ('cybrary', 'Cybrary'),
        ('cisco', 'Cisco'),
        ('tryhackme', 'TryHackMe'),
        ('other', 'Autre'),
    ], default='other')

    def __str__(self):
        return self.name

class Badge(models.Model):
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    image = models.ImageField(upload_to='badges/')
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=[
        ('microsoft', 'Microsoft Learn'),
        ('cybrary', 'Cybrary'),
        ('tryhackme', 'TryHackMe'),
        ('python', 'Python'),
        ('iot', 'IoT'),
        ('other', 'Autre'),
    ], default='other')

    def __str__(self):
        return self.name

class TechStack(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default="#007bff")

    def __str__(self):
        return self.name

class ProjectUpdate(models.Model):
    """Suivi des mises à jour de projets"""
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='updates')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Update pour {self.project.title} - {self.created_at}"

class ProjectComment(models.Model):
    """Commentaires sur les projets"""
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Commentaire de {self.name} sur {self.project.title}"
