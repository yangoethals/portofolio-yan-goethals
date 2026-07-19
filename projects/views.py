from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Project
from core.models import TechStack

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 6

    def get_queryset(self):
        queryset = Project.objects.all().order_by('-order', '-created_at')
        tech = self.request.GET.get('tech')
        if tech:
            queryset = queryset.filter(technologies__name=tech)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tech_stack'] = TechStack.objects.all()
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'projects/project_form.html'
    fields = ['title', 'subtitle', 'description', 'short_description', 'image', 'video', 'video_url', 'github_link', 'demo_link', 'status', 'technologies', 'order', 'featured']
    success_url = reverse_lazy('projects:project_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "Accès non autorisé.")
            return redirect('core_admin:login')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, "✅ Projet créé avec succès !")
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'projects/project_form.html'
    fields = ['title', 'subtitle', 'description', 'short_description', 'image', 'video', 'video_url', 'github_link', 'demo_link', 'status', 'technologies', 'order', 'featured']
    success_url = reverse_lazy('projects:project_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "Accès non autorisé.")
            return redirect('core_admin:login')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, "✅ Projet mis à jour avec succès !")
        return super().form_valid(form)

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('projects:project_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "Accès non autorisé.")
            return redirect('core_admin:login')
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "✅ Projet supprimé avec succès !")
        return super().delete(request, *args, **kwargs)
