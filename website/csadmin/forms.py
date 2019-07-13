from django import forms
from django.contrib.auth.models import User

from .models import Account
from .models import interests


class AccountForm(forms.ModelForm):
    class Meta:
        model=Account
        fields='__all__'

class NewUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('username','password','first_name','last_name','email')

class FDUpdateForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=('username','fdcapital','fdmaturitydate')

class ShareUpdateForm(forms.Form):
    fshareupdate=forms.FloatField()

class ShareDividendForm(forms.ModelForm):
    fsharedividend=forms.FloatField()
    class Meta:
        model=interests
        fields=('sharedividend',)

class CDDividendForm(forms.Form):
    fcddividend=forms.FloatField()

class LongLoanForm(forms.Form):
    flongloaninterest=forms.FloatField()

class EmergencyLoanForm(forms.Form):
    femergencylaoninterest=forms.FloatField()

class FDInterestForm(forms.Form):
    ffdinterest=forms.FloatField()

class MessengerForm(forms.Form):
    fmessage=forms.CharField(widget=forms.TextInput)

class SecretkeyForm(forms.Form):
    fchairmankey=forms.IntegerField()
    fsecretarykey=forms.IntegerField()
