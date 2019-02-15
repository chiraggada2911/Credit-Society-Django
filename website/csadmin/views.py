from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from status.models import Account,Loan,FixedDeposits,Shares,User,Department
from django.forms import ModelForm
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.views import generic


# Create your views here.
def index(request):
    return render (request,'index.html')


@login_required
def commander(request):
    context={
        'dashb':"active"
    }
    return render (request,'console.html',context=context)

@login_required
def members(request):
    users=User.objects.all
    accounts=Account.objects.all
    context={
        'users':users,
        'accounts':accounts,
        'member':"active"
    }
    return render (request,'members.html',context=context)

@login_required
def bank(request):
    fixedDeposits=FixedDeposits.objects.all
    context={
        'fixedDeposits':fixedDeposits,
        'Bank':"active"
    }
    return render (request,'bank.html',context=context)

@login_required
def loansadmin(request):
    loans=Loan.objects.all
    context={
        'loans':loans,
        'loan':"active"
    }
    return render (request,'loansadmin.html',context=context)

@login_required
def totalmoney(request):
    context={
        'money':"active"
    }
    return render (request,'totalmoney.html',context=context)

#class adduseraccountform(ModelForm):
class UserCreate(CreateView):
        model=User
        fields=['first_name','last_name','username','email','password']
        #make_password(password)
        success_url=reverse_lazy('csadmin:account_create')

class AccountCreate(CreateView):
        model=Account
        fields='__all__'
        success_url=reverse_lazy('csadmin:members')

class Fdadd(CreateView):
        model=FixedDeposits
        fields='__all__'
        success_url=reverse_lazy('csadmin:members')

class Loanadd(CreateView):
        model=Loan
        fields='__all__'
        success_url=reverse_lazy('csadmin:members')

class Sharesadd(CreateView):
        model=Shares
        fields='__all__'
        success_url=reverse_lazy('csadmin:members')
