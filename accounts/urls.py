from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('save_drawing/', views.save_drawing, name='save_drawing'),
]
