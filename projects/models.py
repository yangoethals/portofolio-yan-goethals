from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField

class Project(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Terminé'),
        ('in_progress', 'En cours'),
        ('planned', 'Planifié'),
    ]
    
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    description = RichTextField()
    short_description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='projects/images/')
    video = models.FileField(upload_to='projects/videos/', null=True, blank=True)
    video_url = models.URLField(blank=True, help_text="URL YouTube ou Vimeo")
    github_link = models.URLField(blank=True)
    demo_link = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    technologies = models.ManyToManyField('core.TechStack')
    order = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='extra_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/extra/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image de {self.project.title}"
