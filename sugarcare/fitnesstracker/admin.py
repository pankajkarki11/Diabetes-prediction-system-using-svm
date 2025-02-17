from django.contrib import admin

# Register your models here.
from .models import UserProfile, DailyData, ModuleCompletion, FoodLog, RiskAssessment

admin.site.register(UserProfile)
admin.site.register(DailyData)
admin.site.register(ModuleCompletion)
admin.site.register(FoodLog)
admin.site.register(RiskAssessment)



