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

class ShareUpdateForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=('username','fdcapital','fdmaturitydate')

class LongLoanUpdateForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=('username','islongloantaken','longloanamount','longloanperiod')

class EmerLoanUpdateForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=('username','isloanemertaken','emerloanamount','emerloanperiod')

#<<interests form>>

class ShareDividendForm(forms.ModelForm):
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
#<<interest forms end>>


class MessengerForm(forms.Form):
    fmessage=forms.CharField(widget=forms.TextInput)

class SecretkeyForm(forms.Form):
    fchairmankey=forms.IntegerField()
    fsecretarykey=forms.IntegerField()
