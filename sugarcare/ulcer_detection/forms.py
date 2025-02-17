from django import forms

class FootUlcerForm(forms.Form):
    image = forms.ImageField(label='Upload Foot Image', required=True)

