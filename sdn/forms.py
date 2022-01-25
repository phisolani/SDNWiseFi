from django import forms
from .models import Tenant, Controller, Graph


class TenantForm(forms.ModelForm):

    class Meta:
        model = Tenant
        fields = '__all__'


class ControllerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Controller
        fields = '__all__'


class GraphForm(forms.ModelForm):

    class Meta:
        model = Graph
        fields = '__all__'