from django.urls import path
from . import views

app_name = 'core_admin'

urlpatterns = [
    path('login/', views.admin_login_view, name='login'),
    path('logout/', views.admin_logout_view, name='logout'),
    path('dashboard/', views.admin_dashboard_view, name='dashboard'),
    
    # Profil
    path('profile/', views.profile_update_view, name='profile_update'),
    
    # Gestion des compétences
    path('skill/add/', views.AdminSkillCreateView.as_view(), name='skill_add'),
    path('network-skill/add/', views.AdminNetworkSkillCreateView.as_view(), name='network_skill_add'),
    path('cyber-skill/add/', views.AdminCyberSkillCreateView.as_view(), name='cyber_skill_add'),
    path('ai-skill/add/', views.AdminAISkillCreateView.as_view(), name='ai_skill_add'),
    path('devops-skill/add/', views.AdminDevOpsSkillCreateView.as_view(), name='devops_skill_add'),
    
    # Gestion des certificats
    path('certificates/', views.certificate_list_view, name='certificate_list'),
    path('certificates/add/', views.CertificateCreateView.as_view(), name='certificate_add'),
    path('certificates/<int:pk>/update/', views.CertificateUpdateView.as_view(), name='certificate_update'),
    path('certificates/<int:pk>/delete/', views.CertificateDeleteView.as_view(), name='certificate_delete'),
]
