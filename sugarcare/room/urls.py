from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='rooms'),
    path('create-room/', views.create_room, name='create-room'),
    path('<str:room_name>/', views.room, name='room'),
    path('send-message/', views.send_message, name='send_message'),
]
