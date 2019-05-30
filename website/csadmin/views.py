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
from datetime import datetime, date
import datetime

#send_mail
from django.core.mail import send_mail
import smtplib

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
                # subject = 'Admin wants to make some changes'
                # message = Accountholder.name +" : "+ sharedividend
                # email_from = settings.EMAIL_HOST_USER
                #
                # recipient_list = ['jatinhdalvi@gmail.com','aashulikabra@gmail.com','champtem11@gmail.com']
                #
                # send_mail( subject, message, email_from, recipient_list )
                # print("mail sent")
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
    success_url = reverse_lazy('csadmin:account_create')

    def form_valid(self, form):
        valid = super(UserCreate, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        return valid


class AccountCreate(CreateView):
        model=Account
        template_name = 'AccountCreate.html'
        fields=['accountnumber','username','name','sapid','dateofjoining','sharevalue','sharesstartingnumber','sharesendingnumber',]
        success_url=reverse_lazy('csadmin:members')

class FDUpdate(UpdateView):
        model=Account
        fields=['username','fdcapital','fdmaturitydate']
        success_url=reverse_lazy('csadmin:bank')

class LoanUpdate(UpdateView):
        model=Account
        fields=['username','isloanloantaken','isloanemertaken','longloanamount','longloanperiod']
        success_url=reverse_lazy('csadmin:members')

class SharesUpdate(UpdateView):
        model=Account
        fields=['username','sharevalue']
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
def calcinvest():
    Members=Account.objects.all()
    Interests=interests.objects.get(id=1)
    for i in  Members.iterator():
        if(i.sharevalue==0 and i.shareamount==0):
            i.sharevalue=i.cdamount
        elif(i.sharevalue==0 and i.cdamount==0):
            i.sharevalue=i.shareamount
        if(i.totalinvestment==0):
            i.totalinvestment=i.sharebalance+i.cdbalance


        i.totalinvestment=i.totalinvestment+(i.sharevalue)
        if (i.totalinvestment >= 50000):
            i.cdbalance = i.totalinvestment - 50000
            i.sharebalance = 50000
            i.cdamount=i.sharevalue
            i.shareamount=0
        else:
            i.sharebalance=i.totalinvestment
            i.cdbalance=0
            i.shareamount=i.sharevalue
            i.cdamount=0
        print("shareamount")
        print(i.shareamount)
        i.save()

@cron_task(crontab="* * * * *")
def longloan():
    Members=Account.objects.all()
    Interests=interests.objects.get(id=1)
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
                i.loanloanemi=EMI
                interestamount=R*A
                print(interestamount)
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


@cron_task(crontab="* * * * *")
def emergencyloan():
    Members=Account.objects.all()
    Interests=interests.objects.get(id=1)
    sharebalance = 0
    cdbalance = 0

    #Emergencyloan parameters
    Rate=Interests.emerloaninterest
    R=Rate/(12*100) #rate of interest for each month

    for i in  Members.iterator():
        N=i.emerloanperiod
        A=i.emerloanamount
        print(N)
        print(A)
        if(N!=0):
            if(i.emerloanbalance==0):
                EMI=(A*R*(1+R)*N)/(((1+R)*N)-1)
                interestamount=R*A
                i.emerloaninterestamount=interestamount
                print(interestamount)
                principle=EMI-interestamount
                i.emerloanprinciple=principle
                print(principle)
                i.emerloanbalance=i.emerloanamount-principle
                print(i.emerloanbalance)
            else:
                EMI=(A*R*(1+R)*N)/(((1+R)*N)-1)
                print(EMI)
                interestamount=R*i.emerloanbalance
                i.emerloaninterestamount=interestamount
                print(interestamount)
                principle=EMI-interestamount
                i.emerloanprinciple=principle
                print(principle)
                i.emerloanbalance=i.emerloanbalance-principle
        i.totalamount=i.shareamount+i.cdamount+i.longloanprinciple+i.longloaninterestamount+i.emerloanprinciple+i.emerloaninterestamount
        i.save()

@cron_task(crontab="* * * * *")
def fdemail():
    Members=Account.objects.all()
    datetoday=datetime.date.today()
    for i in  Members.iterator():
        print("start")
        date_diff_fd = (relativedelta.relativedelta(i.fdmaturitydate,datetoday))
        print(date_diff_fd)
        if (date_diff_fd.months==+1 and date_diff_fd.days==0 and date_diff_fd.years==0):
            subject = 'FD is getting matured soon'
            message = "Dear sir/ma'am your DJSCOE CS FD is getting matured on " + str(i.fdmaturitydate) + "what wolud you like to do? reply on this email or contact Admin"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['jatinhdalvi@gmail.com','aashulikabra@gmail.com','champtem11@gmail.com']
            send_mail( subject, message, email_from, recipient_list )
            print("mail sent for maturity if FD")
