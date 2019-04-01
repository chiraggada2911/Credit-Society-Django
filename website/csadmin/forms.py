from django import forms
from django.contrib.auth.models import User

from .models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model=Account
        fields='__all__'

class change_ROI_dividend(forms.Form):
    
    new_ROI_dividend = forms.FloatField()
