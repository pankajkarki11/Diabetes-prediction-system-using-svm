from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.IntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True, blank=True)




class DailyData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(unique=True)
    steps = models.PositiveIntegerField()
    calories_burned = models.DecimalField(max_digits=6, decimal_places=2,default=0.0)
    calories_intake = models.DecimalField(max_digits=6, decimal_places=2,default=0.0)

    def __str__(self):
        return f"{self.user.username}'s Daily Data - {self.date}"

class ModuleCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.module} ({'Completed' if self.completed else 'Not Completed'})"
    

class FoodLog(models.Model):
    food_name = models.CharField(max_length=100)
    calories = models.FloatField()
    protein = models.FloatField()
    sugar = models.FloatField()
    fat = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class RiskAssessment(models.Model):
    age = models.IntegerField()
    bmi = models.FloatField()
    family_history = models.BooleanField()
    physical_activity = models.CharField(max_length=50, choices=[('low', 'Low'), ('moderate', 'Moderate'), ('high', 'High')])
    smoking = models.BooleanField()
    alcohol_consumption = models.BooleanField()
    risk_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Risk Assessment for Age: {self.age}"



