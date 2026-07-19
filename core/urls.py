from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('certificates/', views.CertificatesView.as_view(), name='certificates'),
    path('network-skills/', views.NetworkSkillsView.as_view(), name='network_skills'),
    path('cyber-security/', views.CyberSecuritySkillsView.as_view(), name='cyber_security'),
    path('ai-skills/', views.AISkillsView.as_view(), name='ai_skills'),
    path('devops-skills/', views.DevOpsSkillsView.as_view(), name='devops_skills'),
    path('bloque/', views.blocked_view, name='blocked'),
]
