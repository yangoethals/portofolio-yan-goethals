from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import (
    Profile, Skill, Experience, Education, Certificate, Badge, TechStack,
    NetworkSkill, CyberSecuritySkill, AISkill, DevOpsSkill, ProjectUpdate, ProjectComment
)
from projects.models import Project
from blog.models import Post

# ====================
# INTERFACE CLIENT (PUBLIC)
# ====================

class HomeView(TemplateView):
    template_name = 'client/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        context['skills'] = Skill.objects.all().order_by('order')
        context['network_skills'] = NetworkSkill.objects.all().order_by('order')
        context['cyber_skills'] = CyberSecuritySkill.objects.all().order_by('order')
        context['ai_skills'] = AISkill.objects.all().order_by('order')
        context['devops_skills'] = DevOpsSkill.objects.all().order_by('order')
        context['experiences'] = Experience.objects.all().order_by('-order', '-start_date')
        context['educations'] = Education.objects.all().order_by('-start_date')
        context['certificates'] = Certificate.objects.all()
        context['badges'] = Badge.objects.all()
        context['tech_stack'] = TechStack.objects.all()
        context['featured_projects'] = Project.objects.filter(featured=True)[:3]
        context['latest_posts'] = Post.objects.filter().order_by('-published_at')[:3]
        
        # STATISTIQUES - COMPTAGES DIRECTS
        context['projects_count'] = Project.objects.count()
        context['experiences_count'] = Experience.objects.count()
        context['certificates_count'] = Certificate.objects.count()
        context['badges_count'] = Badge.objects.count()
        
        return context

class AboutView(TemplateView):
    template_name = 'client/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()
        context['skills'] = Skill.objects.all().order_by('order')
        context['network_skills'] = NetworkSkill.objects.all().order_by('order')
        context['cyber_skills'] = CyberSecuritySkill.objects.all().order_by('order')
        context['ai_skills'] = AISkill.objects.all().order_by('order')
        context['devops_skills'] = DevOpsSkill.objects.all().order_by('order')
        context['tech_stack'] = TechStack.objects.all()
        context['certificates'] = Certificate.objects.all()
        context['badges'] = Badge.objects.all()
        return context

class CertificatesView(TemplateView):
    template_name = 'client/certificates.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['certificates'] = Certificate.objects.all()
        context['badges'] = Badge.objects.all()
        return context

class NetworkSkillsView(TemplateView):
    template_name = 'client/network_skills.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['network_skills'] = NetworkSkill.objects.all().order_by('order')
        context['profile'] = Profile.objects.first()
        return context

class CyberSecuritySkillsView(TemplateView):
    template_name = 'client/cyber_security.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cyber_skills'] = CyberSecuritySkill.objects.all().order_by('order')
        context['profile'] = Profile.objects.first()
        return context

class AISkillsView(TemplateView):
    template_name = 'client/ai_skills.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ai_skills'] = AISkill.objects.all().order_by('order')
        context['profile'] = Profile.objects.first()
        return context

class DevOpsSkillsView(TemplateView):
    template_name = 'client/devops_skills.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['devops_skills'] = DevOpsSkill.objects.all().order_by('order')
        context['profile'] = Profile.objects.first()
        return context

# ====================
# INTERFACE ADMIN (GESTION)
# ====================

def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('core_admin:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            messages.success(request, "✅ Connexion réussie !")
            return redirect('core_admin:dashboard')
        else:
            messages.error(request, "❌ Identifiants incorrects.")
    
    return render(request, 'admin/login.html')

def admin_logout_view(request):
    logout(request)
    messages.success(request, "✅ Déconnecté avec succès.")
    return redirect('core_admin:login')

@login_required
def admin_dashboard_view(request):
    if not request.user.is_superuser:
        messages.error(request, "Accès non autorisé.")
        return redirect('core:home')
    
    profile = Profile.objects.first()
    context = {
        'profile': profile,
        'projects_count': Project.objects.count(),
        'skills_count': Skill.objects.count(),
        'network_skills_count': NetworkSkill.objects.count(),
        'cyber_skills_count': CyberSecuritySkill.objects.count(),
        'ai_skills_count': AISkill.objects.count(),
        'devops_skills_count': DevOpsSkill.objects.count(),
        'certificates_count': Certificate.objects.count(),
        'badges_count': Badge.objects.count(),
        'recent_projects': Project.objects.all().order_by('-created_at')[:5],
    }
    return render(request, 'admin/dashboard.html', context)

# === Gestion des Compétences ===

class AdminSkillCreateView(CreateView):
    model = Skill
    template_name = 'admin/skill_form.html'
    fields = ['name', 'category', 'icon', 'level', 'order']
    success_url = reverse_lazy('core_admin:dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, "Accès non autorisé.")
            return redirect('core_admin:login')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, "✅ Compétence ajoutée !")
        return super().form_valid(form)

class AdminNetworkSkillCreateView(CreateView):
    model = NetworkSkill
    template_name = 'admin/network_skill_form.html'
    fields = ['name', 'description', 'icon', 'level', 'order']
    success_url = reverse_lazy('core_admin:dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, "Accès non autorisé.")
            return redirect('core_admin:login')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, "✅ Compétence réseau ajoutée !")
        return super().form_valid(form)

class AdminCyberSkillCreateView(CreateView):
    model = CyberSecuritySkill
    template_name = 'admin/cyber_skill_form.html'
    fields = ['name', 'description', 'icon', 'level', 'order']
    success_url = reverse_lazy('core_admin:dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, "Accès non autorisé.")
            return redirect('core_admin:login')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, "✅ Compétence cybersécurité ajoutée !")
        return super().form_valid(form)

class AdminAISkillCreateView(CreateView):
    model = AISkill
    template_name = 'admin/ai_skill_form.html'
    fields = ['name', 'category', 'description', 'icon', 'level', 'order']
    success_url = reverse_lazy('core_admin:dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, "Accès non autorisé.")
            return redirect('core_admin:login')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, "✅ Compétence IA ajoutée !")
        return super().form_valid(form)

class AdminDevOpsSkillCreateView(CreateView):
    model = DevOpsSkill
    template_name = 'admin/devops_skill_form.html'
    fields = ['name', 'description', 'icon', 'level', 'order']
    success_url = reverse_lazy('core_admin:dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, "Accès non autorisé.")
            return redirect('core_admin:login')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, "✅ Compétence DevOps ajoutée !")
        return super().form_valid(form)

# === Gestion du Profil ===

@login_required
def profile_update_view(request):
    if not request.user.is_superuser:
        messages.error(request, "Accès non autorisé.")
        return redirect('core_admin:login')
    
    profile = Profile.objects.first()
    if not profile:
        profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Profil mis à jour avec succès !")
            return redirect('core_admin:dashboard')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'admin/profile_form.html', {'form': form, 'profile': profile})

# === Gestion des Certificats ===

class CertificateCreateView(LoginRequiredMixin, CreateView):
    model = Certificate
    template_name = 'admin/certificate_form.html'
    fields = ['name', 'issuer', 'date', 'credential_url', 'image', 'description', 'category']
    success_url = reverse_lazy('core_admin:certificate_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "Accès non autorisé.")
            return redirect('core_admin:login')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, "✅ Certificat ajouté avec succès !")
        return super().form_valid(form)

class CertificateUpdateView(LoginRequiredMixin, UpdateView):
    model = Certificate
    template_name = 'admin/certificate_form.html'
    fields = ['name', 'issuer', 'date', 'credential_url', 'image', 'description', 'category']
    success_url = reverse_lazy('core_admin:certificate_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "Accès non autorisé.")
            return redirect('core_admin:login')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, "✅ Certificat mis à jour avec succès !")
        return super().form_valid(form)

class CertificateDeleteView(LoginRequiredMixin, DeleteView):
    model = Certificate
    template_name = 'admin/certificate_confirm_delete.html'
    success_url = reverse_lazy('core_admin:certificate_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "Accès non autorisé.")
            return redirect('core_admin:login')
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "✅ Certificat supprimé avec succès !")
        return super().delete(request, *args, **kwargs)

def certificate_list_view(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "Accès non autorisé.")
        return redirect('core_admin:login')
    
    certificates = Certificate.objects.all().order_by('-date')
    return render(request, 'admin/certificate_list.html', {'certificates': certificates})

# Vue pour les utilisateurs bloqués
def blocked_view(request):
    return render(request, 'core/blocked.html', status=403)

# Import du formulaire
from .forms import ProfileForm
