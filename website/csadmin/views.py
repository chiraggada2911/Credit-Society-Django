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
from django.shortcuts import redirect
from django.template.loader import get_template
from django.contrib.auth.models import User

#for background tasks
from autotask.tasks import cron_task

#for date and time
from datetime import datetime
from dateutil import relativedelta

#Background

#forms
from django.forms import ModelForm
from csadmin.forms import ShareDividendForm,CDDividendForm,LongLoanForm,EmergencyLoanForm,FDInterestForm,NewUserForm

# Create your views here.
def index(request):
    return render (request,'index.html')


@login_required
def commander(request):
    Members=Account.objects.all()
    context={
        'dashb':"active",
        'Members':Members,
    }
    return render (request,'console.html',context=context)


@login_required
def members(request):
    Members=Account.objects.all()
    Interests=interests.objects.get(id=1)
    context={
        'Members':Members,
        'Interests':Interests,
        'member':"active"
    }
    return render (request,'members.html',context=context)

@login_required
def bank(request):
    Banks=Account.objects.all
    Interests=interests.objects.all
    context={
        'Banks':Banks,
        'Interests':Interests,
        'Bank':"active"
    }
    return render (request,'bank.html',context=context)

@login_required
def loansadmin(request):
    Loansadmin=Account.objects.all
    Interests=interests.objects.all
    context={
        'Loansadmin':Loansadmin,
        'Interests':Interests,
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
                t=interests.objects.first()
                t.sharedividend=sharedividend
                t.save()
                print("valid_share+saved")
        elif 'btncd' in request.POST:
            tcddividend=CDDividendForm(request.POST)
            print("POST_2")
            if tcddividend.is_valid():
                cddividend = tcddividend.cleaned_data['fcddividend']
                t=interests.objects.first()
                t.cddividend=cddividend
                t.save()
                print("valid_cd")
        elif 'btnlongloan' in request.POST:
            tlongloaninterest=LongLoanForm(request.POST)
            print("POST_3")
            if tlongloaninterest.is_valid():
                longloaninterest = tlongloaninterest.cleaned_data['flongloaninterest']
                t=interests.objects.first()
                t.longloaninterest=longloaninterest
                t.save()
                print("valid_longloan")
        elif 'btnemerloan' in request.POST:
            temergencyloaninterest=EmergencyLoanForm(request.POST)
            print("POST_4")
            if temergencyloaninterest.is_valid():
                emergencyloaninterest = temergencyloaninterest.cleaned_data['femergencylaoninterest']
                t=interests.objects.first()
                t.emerloaninterest=emergencyloaninterest
                t.save()
                print("valid_emerloan")
        elif 'btnfd' in request.POST:
            tfdinterest=FDInterestForm(request.POST)
            print("POST_5")
            if tfdinterest.is_valid():
                fdinterest = tfdinterest.cleaned_data['ffdinterest']
                t=interests.objects.first()
                t.fdinterest=fdinterest
                t.save()
                print("valid_fd")

    context={
        'money':"active"
    }
    return render (request,'totalmoney.html',context=context)

class UserCreate(CreateView):
    template_name = 'UserCreate.html'
    form_class = NewUserForm
    success_url = 'account_create'

    def form_valid(self, form):
        valid = super(UserCreate, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        return valid


class AccountCreate(CreateView):
        model=Account
        fields=['accountnumber','username','name','sapid','dateofjoining','shareamount','sharesstartingnumber','sharesendingnumber',]
        success_url=reverse_lazy('csadmin:members')

class FDUpdate(UpdateView):
        model=Account
        fields=['username','fdcapital','fdmaturitydate']
        success_url=reverse_lazy('csadmin:bank')

class LoanUpdate(UpdateView):
        model=Account
        fields=['username','isloantaken','longloanamount','longloanperiod']
        success_url=reverse_lazy('csadmin:members')

class SharesUpdate(UpdateView):
        model=Account
        fields=['user''shareamount']
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

@cron_task(crontab="* * * * *")
def clean_up():
    Members=Account.objects.all()
    Interests=interests.objects.get(id=1)
    sharebalance = 0
    cdbalance = 0

    #loan parameters
    Rate=Interests.longloaninterest
    R=Rate/(12*100) #rate of interest for each month

    for i in  Members.iterator():
        N=i.longloanperiod
        A=i.longloanamount
        print(N)
        print(A)
        if(N!=0):
            if(i.longloanbalance==0):
                EMI=(A*R*(1+R)**N)/(((1+R)**N)-1)
                print(EMI)
                interestamount=R*A
                i.longloaninterestamount=interestamount
                print(interestamount)
                principle=EMI-interestamount
                i.longloanprinciple=principle
                print(principle)
                i.longloanbalance=i.longloanamount-principle
                print(i.longloanbalance)
            else:
                EMI=(A*R*(1+R)**N)/(((1+R)**N)-1)
                print(EMI)
                interestamount=R*i.longloanbalance
                i.longloaninterestamount=interestamount
                print(interestamount)
                principle=EMI-interestamount
                i.longloanprinciple=principle
                print(principle)
                i.longloanbalance=i.longloanbalance-principle
        i.save()

        #
        # date = i.dateofjoining
        # datetoday=datetime.date.today()
        # days=relativedelta.relativedelta(datetoday,date)
        # nod=days.months
        # year = days.years
        # final = nod + 12 * year
        # totalInvestment = final * (i.sharevalue)

        # totalInvestment=i.totalamount+(i.sharevalue)
        #
        # if totalInvestment >= 50000:
        #     cdbalance = totalInvestment - 50000
        #     sharebalance = 50000
        #     i.sharebalance=sharebalance
        #     i.cdbalance=cdbalance
        #     i.cdamount=i.sharevalue
        #     i.shareamount=0
        # else:
        #     i.sharebalance=totalInvestment
        #     i.cdbalance=cdbalance
        #     i.shareamount=i.sharevalue
        #     i.cdamount=0
        # i.totalamount=totalInvestment
        # print("shareamount")
        # print(i.shareamount)
