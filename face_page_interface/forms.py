from django import forms
from .models import CustomUser

class BioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        exclude = ['user']