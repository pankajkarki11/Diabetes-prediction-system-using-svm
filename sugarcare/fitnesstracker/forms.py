from django import forms
from .models import RiskAssessment

class FoodInputForm(forms.Form):
    food_name = forms.CharField(label="Food Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))


class RiskAssessmentForm(forms.ModelForm):
    class Meta:
        model = RiskAssessment
        fields = ['age', 'bmi', 'family_history', 'physical_activity', 'smoking', 'alcohol_consumption']
        widgets = {
            'physical_activity': forms.Select(attrs={'class': 'form-control'}),
        }

