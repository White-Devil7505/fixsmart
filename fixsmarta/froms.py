# forms.py
from django import forms
from .models import SmartFix

class RegisterForm(forms.ModelForm):
    class Meta:
        model = SmartFix
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
        }
