from django.urls import path
from . import views

app_name = 'blog'  # Ceci définit le namespace

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]
