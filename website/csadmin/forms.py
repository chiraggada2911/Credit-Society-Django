from django import forms
from django.contrib.auth.models import User
from status.models import Account,interests,Notification,FixedDeposits,HistorylongLoan,HistoryemerLoan,HistoryFd

class InterestsForm(forms.ModelForm):
    class Meta:
        model=interests
        fields=('sharedividend','cddividend','fdinterest','emerloaninterest','longloaninterest','year')

class AccountForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=('accountnumber','username','name','sapid','dateofjoining','teachingstaff','nonteachingstaff','sharevalue')

class NewUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('username','password','first_name','last_name','email')

class FDUpdateForm(forms.ModelForm):
    class Meta:
        model=FixedDeposits
        fields=('username','fdcapital','fdmaturitydate')

class ShareUpdateForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=('username','sharevalue')

class LongLoanUpdateForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=('username','longloanamount','longloanperiod','longloanadditional','longloandate')

class EmerLoanUpdateForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=('username','emerloanamount','emerloanperiod','emerloandate')

class DownPaymentForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=('username','downpayment')

class MessengerForm(forms.Form):
    fmessage=forms.CharField(widget=forms.TextInput)

class SecretkeyForm(forms.Form):
    fchairmankey=forms.IntegerField()
    fsecretarykey=forms.IntegerField()
