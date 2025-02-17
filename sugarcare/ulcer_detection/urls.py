from django.urls import path
from . import views

urlpatterns = [
    path('', views.ulcer_detection_view, name='ulcer_detection'),
]