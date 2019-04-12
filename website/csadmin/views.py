from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from status.models import Account,interests
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
from csadmin.forms import ShareDividendForm,CDDividendForm,LongLoanForm,EmergencyLoanForm,FDInterestForm

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
    Members=Account.objects.all
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
        'Members':Members,
        'member':"active"
    }
    return render (request,'members.html',context=context)

@login_required
def bank(request):
    Banks=Account.objects.all
    context={
        'Banks':Banks,
        'Bank':"active"
    }
    return render (request,'bank.html',context=context)

@login_required
def loansadmin(request):
    Loansadmin=Account.objects.all
    context={
        'Loansadmin':Loansadmin,
        'loan':"active"
    }
    return render (request,'loansadmin.html',context=context)

@login_required
def totalmoney(request):
    sharedividend=0
    cddividend=0
    longloaninterest=0
    emergencyloaninterest=0
    fdinterest=0
    if request.method=="POST":
        if 'btnshare' in request.POST:
            tsharedividend=ShareDividendForm(request.POST)
            print("POST_1")
            if tsharedividend.is_valid():
                sharedividend = tsharedividend.cleaned_data['fsharedividend']
                t=interests.objects.get(id=1)
                t.sharedividend=sharedividend
                t.save()
                print("valid_share+saved")
        elif 'btncd' in request.POST:
            tcddividend=CDDividendForm(request.POST)
            print("POST_2")
            if tcddividend.is_valid():
                cddividend = tcddividend.cleaned_data['fcddividend']
                print("valid_cd")
        elif 'btnlongloan' in request.POST:
            tlongloaninterest=LongLoanForm(request.POST)
            print("POST_3")
            if tlongloaninterest.is_valid():
                longloaninterest = tlongloaninterest.cleaned_data['flongloaninterest']
                print("valid_longloan")
        elif 'btnemerloan' in request.POST:
            temergencyloaninterest=EmergencyLoanForm(request.POST)
            print("POST_4")
            if temergencyloaninterest.is_valid():
                emergencyloaninterest = temergencyloaninterest.cleaned_data['femergencylaoninterest']
                print("valid_emerloan")
        elif 'btnfd' in request.POST:
            tfdinterest=FDInterestForm(request.POST)
            print("POST_5")
            if tfdinterest.is_valid():
                fdinterest = tfdinterest.cleaned_data['ffdinterest']
                print("valid_fd")

    context={
        'money':"active"
    }
    return render (request,'totalmoney.html',context=context)

#class adduseraccountform(ModelForm):
class UserCreate(CreateView):
        #model=User
        fields=['first_name','last_name','username','email','password']
        #make_password(password)
        success_url=reverse_lazy('csadmin:account_create')

class AccountCreate(CreateView):
        model=Account
        fields=['accountnumber','username','name','sapid','dateofjoining','shareamount','cdamount',]
        success_url=reverse_lazy('csadmin:members')

class Fdadd(CreateView):
        #model=FixedDeposits
        fields='__all__'
        success_url=reverse_lazy('csadmin:members')

class Loanadd(CreateView):
        model=Account
        fields=['isloantaken','longloanamount']
        success_url=reverse_lazy('csadmin:members')

class Sharesadd(CreateView):
        model=Account
        fields=['sharesstartingnumber','sharesendingnumber']
        success_url=reverse_lazy('csadmin:members')

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        template = get_template('tableview.html')
        accounts=Account.objects.all
        context ={
            'accounts':accounts,
        }
        html = template.render(context)
        pdf = render_to_pdf('tableview.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
