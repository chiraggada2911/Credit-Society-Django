from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','email','password']

class change_MoneyForm(forms.Form):
    new_amount = forms.IntegerField()

Loan_choice=[
    ('normal_loan','Normal Loan'),
    ('emergency_loan', 'Emergency Loan'),
]

class LoanReqForm(forms.Form):

    loanChoice = forms.CharField(widget=forms.RadioSelect(choices=Loan_choice))
    loanAmount = forms.IntegerField()
