from django.urls import path
from .import views

urlpatterns=[
  path('',views.track_activity,name='dashboard'),
  path("food-nutrition/", views.food_nutrition_view, name="food_nutrition"),
  path('risk-calculator/', views.risk_calculator_view, name='risk_calculator'),
]