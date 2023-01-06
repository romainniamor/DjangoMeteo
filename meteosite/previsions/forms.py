from django import forms
from django.forms import ModelChoiceField
from .models import Departement



class DepartementModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nom

class VilleForm(forms.Form):
    nom = forms.CharField(label='Nom', max_length=40, required=True)
    code_postal = forms.IntegerField(widget=forms.TextInput, label='Code_postal', required=True)
    departement = DepartementModelChoiceField(label='Departement', required=True,
                                              queryset=Departement.objects.all(),
                                              empty_label="Choisir un département")