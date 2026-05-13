from django import forms
from .models import Projeto


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = '__all__'
