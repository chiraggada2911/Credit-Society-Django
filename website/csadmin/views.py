from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from status.models import Account,Loan,FixedDeposits,Shares,User
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.views import generic
from csadmin.utils import render_to_pdf
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template

#for date and time
import datetime
from dateutil import relativedelta

#forms
from django.forms import ModelForm
from csadmin.forms import change_ROI_dividend

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
    name=str(Account.accountholder)
    #Accountholder=Account.objects.all
    #date = accounts.dateofjoining
    #print("chirag")
    #print(date)


    # datetoday=datetime.date.today()
    # days=relativedelta.relativedelta(datetoday,date)
    # nod=days.months
    # year = days.years
    # final = nod + 12 * year
    # totalInvestment = final * (Account.monthlyDeduction)
    # print(totalInvestment)
    context={
        'users':users,
        'accounts':accounts,
        'name':name,
        'member':"active"
    }
    return render (request,'members.html',context=context)

@login_required
def bank(request):
    fixedDeposits=FixedDeposits.objects.all
    accounts=Account.objects.all
    users=User.objects.all
    name=str(Account.accountholder)
    context={
        'fixedDeposits':fixedDeposits,
        'accounts':accounts,
        'name':name,
        'users':users,
        'Bank':"active"
    }
    return render (request,'bank.html',context=context)

@login_required
def loansadmin(request):
    loans=Loan.objects.all
    accounts=Account.objects.all
    context={
        'loans':loans,
        'accounts':accounts,
        'loan':"active"
    }
    return render (request,'loansadmin.html',context=context)

@login_required
def totalmoney(request):
    final_dividend=0
    if request.method=="POST":
        dividend=change_ROI_dividend(request.POST)
        if dividend.is_valid():
            final_dividend = dividend.cleaned_data['new_ROI_dividend']

        else:
            dividend=change_ROI_dividend()
    print(final_dividend)

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

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        template = get_template('tableview.html')
        users=User.objects.all
        accounts=Account.objects.all
        name=str(Account.accountholder)
        context ={
            'users':users,
            'accounts':accounts,
            'name':name,
        }
        html = template.render(context)
        pdf = render_to_pdf('tableview.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
