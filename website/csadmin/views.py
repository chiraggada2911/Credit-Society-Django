from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
# models
from status.models import Account,interests,Notification,FixedDeposits,HistorylongLoan,HistoryemerLoan,HistoryFd
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
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib import messages

#filter
from .filters import AccountFilter,UserFilter,UsersFilter
#for background tasks
from autotask.tasks import cron_task

#for date and time
from datetime import datetime,date
from dateutil import relativedelta

import datetime

#send_mail
from django.core.mail import send_mail,send_mass_mail
import smtplib

#forms
from django.forms import ModelForm
from csadmin.forms import AccountForm,NewUserForm,MessengerForm,SecretkeyForm,FDUpdateForm,ShareUpdateForm,LongLoanUpdateForm,EmerLoanUpdateForm,DownPaymentForm,InterestsForm

# Create your views here.
def index(request):
    return render (request,'index.html')

# @login_required
# def notisave(notificationmessage,senderid):
#     notification=Notification()
#     notification.notimessage=notificationmessage
#     notification.sender_id=senderid
#     notification.save()

#for history of loans
def longloanhistory(longloanamount,longloandate,longloanperiod,userid):
    Loan=HistorylongLoan()
    Loan.longloanamount=longloanamount
    Loan.longloandate=longloandate
    Loan.longloanperiod=longloanperiod
    Loan.username=userid
    Loan.save()

def emerloanhistory(emerloanamount,emerloandate,emerloanperiod,userid):
    EmerLoan=HistoryemerLoan()
    EmerLoan.emerloanamount=emerloanamount
    EmerLoan.emerloandate=emerloandate
    EmerLoan.emerloanperiod=emerloanperiod
    EmerLoan.username=userid
    EmerLoan.save()

def fdhistory(fdcapital,fddate,fdmaturitydate,userid):
    Fd=HistoryFd()
    Fd.fdcapital=fdcapital
    Fd.fddate=fddate
    Fd.fdmaturitydate=fdmaturitydate
    Fd.username_id=userid
    Fd.save()

@login_required
def index(request):
    Members=Account.objects.all()
    noofnoti=Notification.objects.all().count()
    acc_filter = AccountFilter(request.GET, queryset=Members)
    context={
        'dashb':"active",
        'Members':Members,
        'noofnoti':noofnoti,
        'filter': acc_filter,
    }
    return render (request,'console.html',context=context)


@login_required
def members(request):
    Members=Account.objects.all()
    Interests=interests.objects.all().last()
    noofnoti=Notification.objects.all().count()
    acc_filter = AccountFilter(request.GET, queryset=Members)
    context={
        'Members':Members,
        'Interests':Interests,
        'member':"active",
        'filter': acc_filter,
        'noofnoti':noofnoti,
    }
    return render (request,'members.html',context=context)


@login_required
def fixeddeposits(request):
    users=Account.objects.all()
    userF=FixedDeposits.objects.all().order_by('fdmaturitydate')
    Interests=interests.objects.all().last()
    noofnoti=Notification.objects.all().count()
    foo=FixedDeposits.objects.prefetch_related('username').order_by('fdmaturitydate')
    acc_filter = UserFilter(request.GET, queryset=foo)
    context={
        'fdadmin':users,
        'Interests':Interests,
        'Bank':"active",
        'filter': acc_filter,
        'noofnoti':noofnoti,
        'bo':foo,
    }
    return render (request,'fd_admin.html',context=context)


@login_required
def loansadmin(request):
    Members=Account.objects.all()
    Interests=interests.objects.all().last()
    noofnoti=Notification.objects.all().count()
    acc_filter = AccountFilter(request.GET, queryset=Members)
    context={
        'Loansadmin':Members,
        'Interests':Interests,
        'loan':"active",
        'filter': acc_filter,
        'noofnoti':noofnoti,
    }
    return render (request,'loans_admin.html',context=context)


@login_required
def change(request):

    Interest=interests.objects.all().last()
    noofnoti=Notification.objects.all().count()
    Interests=interests.objects.all
    if request.method=="POST":

        if 'btnverify' in request.POST:
            tsecretkey=SecretkeyForm(request.POST)
            print("POST_1")
            if tsecretkey.is_valid():
                chairmankey=tsecretkey.cleaned_data['fchairmankey']
                print("chairman's key")
                print(chairmankey)
                secretarykey=tsecretkey.cleaned_data['fsecretarykey']
                print("secretary's key")
                print(secretarykey)
                if (chairmankey == 123 and secretarykey ==321):
                    print("Allow")

                    return redirect('/csadmin/interests')
                else:
                    print("Not Allow!!")

    context={
        'Interest':Interest,
        'Interests':Interests,
        'money':"active",
        'noofnoti':noofnoti,
    }

    return render (request,'change.html',context=context)


@login_required
def message(request):
    recievers = []
    user=Account.objects.all
    users = User.objects.all()
    noofnoti=Notification.objects.all().count()
    for i in users.iterator():
        user_email = i.email
        print(user_email)
        recievers.append(i.email)
    if request.method=="POST":
        tmessage=MessengerForm(request.POST)
        if tmessage.is_valid():
            message=tmessage.cleaned_data['fmessage']
            print(message)
            subject = 'This email is from Credit Society Committee'
            email_from = settings.EMAIL_HOST_USER
            send_mass_mail( subject, message, email_from, recievers )
            print("mail sent from messanger")

        else:
            print("error at validity of message")
    context={

        'message':"active",
        'noofnoti':noofnoti,
    }
    return render (request,'messanger.html',context=context)

@login_required
def notifications(request):
    noti=Notification.objects.all()
    noofnoti=Notification.objects.all().count()
    context={
        'noti':noti,
        'notifications':"active",
        'noofnoti':noofnoti,
    }
    return render (request,'notifications_admin.html',context=context)

def notidelete(request,part_id =None):
    object = Notification.objects.get(id=part_id)
    object.delete()
    return redirect('csadmin:notifications')

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
        form_class = AccountForm
        template_name = 'AccountCreate.html'
        success_url=reverse_lazy('csadmin:members')

        def get_context_data(self, **kwargs):
            userU=User.objects.all()
            userA=Account.objects.all().last()
            acc_no=userA.accountnumber + 1
            print(acc_no)
            context = super(CreateView, self).get_context_data(**kwargs)
            context={
                'user':userU,
                'acc_nu':acc_no,
                'date_today':datetime.date.today(),
            }
            return context


class InterestsUpdate(CreateView):
        model=interests
        form_class = InterestsForm
        template_name = 'interests_form.html'
        success_url=reverse_lazy('csadmin:change')

        def get_context_data(self):
            interest=interests.objects.all().last()
            fyear=str(datetime.date.today().year) +"-"+str(datetime.date.today().year+1)
            context={
                'interest':interest,
                'year':fyear,
            }
            return context

        def get_success_url(self):
            recievers=[]
            users = User.objects.all()
            for i in users.iterator():
                user_email = i.email
                print(user_email)
                recievers.append(i.email)
            message="interests rates changed"
            subject = 'This email is from Credit Society Committee'
            email_from = settings.EMAIL_HOST_USER
            send_mail( subject, message, email_from, recievers )
            return reverse_lazy('csadmin:members')

class AccountDelete(DeleteView):
    template_name = 'Userdelete.html'
    success_url=reverse_lazy('csadmin:members')

    def get_object(self):
        id_=self.kwargs.get("id")
        UserA=Account.objects.get(id=id_)
        print(str(UserA) + " User is deleted")
        return get_object_or_404(Account,id=id_)

    def get_success_url(self):
        id_=self.kwargs.get("id")
        UserA=Account.objects.get(id=id_)
        UserU=User.objects.get(pk=UserA.username_id)
        UserU.is_active=False
        UserU.save()
        print(UserU.email)
        message="Dear sir/ma'am your DJSCOE CS account " + str(UserU) + " is deleted by admin"
        subject = 'This email is from Credit Society Committee'
        email_from = settings.EMAIL_HOST_USER
        recievers=[UserU.email]
        send_mail( subject, message, email_from, recievers )
        print("mail sent for deleteing account")
        return reverse_lazy('csadmin:members')


@login_required
def UserDelete(request):
    UserA=Account.objects.all()
    user_filter = AccountFilter(request.GET, queryset=UserA)
    context={
        'User':UserA,
        'filter': user_filter,
    }
    return render (request,'deleteuser.html',context=context)

class Downpayment(UpdateView):
        model=Account
        form_class = DownPaymentForm
        template_name = 'downpayment_form.html'
        success_url=reverse_lazy('csadmin:loansadmin')

        def get_context_data(self, **kwargs):
            id_=self.kwargs.get("pk")
            UserA=Account.objects.get(pk=id_)
            context = super(UpdateView, self).get_context_data(**kwargs)
            print(UserA)
            print('downpayment')
            messages.success(self.request, 'Mail sent')
            context={
                'Userid':UserA.username_id,
                'username':UserA.name,
                'userdownpayment':UserA.downpayment,
            }
            return context

        def get_success_url(self):
            id_=self.kwargs.get("pk")
            UserA=Account.objects.get(pk=id_)
            print(UserA.name)
            residue=UserA.longloanbalance-UserA.downpayment
            UserA.displaydownpayment=UserA.displaydownpayment+UserA.downpayment
            print('downpayment')
            print(residue)
            UserA.longloanbalance=residue
            if (UserA.longloanbalance==0):
                UserA.islongloantaken=False
                UserA.displaydownpayment=0
            UserA.save()
            return reverse_lazy('csadmin:fixeddeposits')

class FDCreate(CreateView):
    model=FixedDeposits
    form_class=FDUpdateForm
    template_name='fixeddeposits_create_form.html'
    success_url=reverse_lazy('csadmin:fixeddeposits')

    def get_context_data(self,**kwargs):
        id_=self.kwargs.get("pk")
        userA=Account.objects.get(pk=id_)
        userU=User.objects.get(pk=userA.username_id)
        idate=date.today()+datetime.timedelta(days=366)
        print(idate)
        context = super(CreateView, self).get_context_data(**kwargs)
        context={
            'username':userA.name,
            'Userid':userU.id,
            'i_date':idate,
        }
        return context

    def get_success_url(self):
        id_=self.kwargs.get("pk")
        userA=Account.objects.get(pk=id_)
        userF=FixedDeposits.objects.all().last()
        fdhistory(userF.fdcapital,userF.fddate,userF.fdmaturitydate,userF.username_id)
        print("All ok")
        print(userF.username)
        return reverse_lazy('csadmin:fixeddeposits')


class FDUpdate(UpdateView):
        model=FixedDeposits
        form_class = FDUpdateForm
        template_name = 'fixeddeposits_update_form.html'
        success_url=reverse_lazy('csadmin:fixeddeposits')

        def get_context_data(self, **kwargs):
            id_=self.kwargs.get("pk")
            UserA=FixedDeposits.objects.get(pk=id_)
            context = super(UpdateView, self).get_context_data(**kwargs)
            print(UserA)
            print('FD update ')
            context={
                'Userid':UserA.username_id,
                'username':UserA.username,
                'userfddate':UserA.fdmaturitydate,
                'userfdamt':UserA.fdcapital,
            }

        def post(self,request,**kwargs):
            id_=self.kwargs.get("pk")
            userF=FixedDeposits.objects.get(pk=id_)
            UserU=User.objects.get(pk=userF.username_id)
            Members=Account.objects.get(username_id=UserU.id)
            Interests=interests.objects.all().last()
            datetoday=datetime.date.today()
            date_diff_fd = (relativedelta.relativedelta(userF.fdmaturitydate,datetoday))

            if "renew_button" in request.POST:
                date_diff_fd = (relativedelta.relativedelta(userF.fdmaturitydate,datetoday))
                print(userF.fdmaturitydate)
                print(type(userF.fdmaturitydate))

                if (userF.fdmaturitydate.year%4==0 and userF.fdmaturitydate.year%100!=0 or userF.fdmaturitydate.year%400==0):
                    userF.fdmaturitydate=userF.fdmaturitydate + datetime.timedelta(days=366)
                    SimpleInterest=userF.fdcapital*Interests.fdinterest/100
                    userF.fdcapital=userF.fdcapital+SimpleInterest
                    message="Dear sir/ma'am your DJSCOE CS account" + str(Members.name) + "Fd is renew and New maturity date is" + str(userF.fdmaturitydate)
                    subject = 'This email is from Credit Society Committee regarding your Fixed Deposit'
                    email_from = settings.EMAIL_HOST_USER
                    recievers=[UserU.email]
                    send_mail(subject,message,email_from,recievers)
                    print("mail sent for FD renewal")
                else:
                    userF.fdmaturitydate=userF.fdmaturitydate + datetime.timedelta(days=365)
                    SimpleInterest=userF.fdcapital*Interests.fdinterest/100
                    userF.fdcapital=userF.fdcapital+SimpleInterest
                    message="Dear sir/ma'am your DJSCOE CS account" + str(Members.name) + "Fd is renew and New maturity date is" + str(userF.fdmaturitydate)
                    subject = 'This email is from Credit Society Committee  regarding your Fixed Deposit'
                    email_from = settings.EMAIL_HOST_USER
                    recievers=[UserU.email]
                    send_mail(subject,message,email_from,recievers)
                    print("mail sent of FD renewal")
                fdhistory(userF.fdcapital,date.today(),userF.fdmaturitydate,userF.username_id)
                userF.save()
                # Members.save()

            if "clr_button" in request.POST:
                print("clear")
                if (date_diff_fd.months==-1 or date_diff_fd.days==-1 or date_diff_fd.years==-1):
                    SimpleInterest=userF.fdcapital*5/100
                    fd_totalpay=userF.fdcapital+SimpleInterest
                    print(fd_totalpay)
                    print("fd totalpay")
                    userF.fdcapital=0
                    userF.fdmaturitydate=None
                    message="Dear sir/ma'am your DJSCOE CS account " + str(Members.name) + " your FD has been cleared and Your total amount is " + str(fd_totalpay)
                    subject = 'This email is from Credit Society Committee regarding your Fixed Deposits'
                    email_from = settings.EMAIL_HOST_USER
                    recievers=[UserU.email]
                    send_mail( subject, message, email_from, recievers )
                    print("mail sent of fdcapital")
                else:
                    SimpleInterest=userF.fdcapital*Interests.fdinterest/100
                    fd_totalpay=userF.fdcapital+SimpleInterest
                    print(fd_totalpay)
                    userF.fdcapital=0
                    userF.fdmaturitydate=None
                    message="Dear sir/ma'am your DJSCOE CS account " + str(Members.name) + " your FD has been cleared and Your total amount is " + str(fd_totalpay)
                    subject = 'This email is from Credit Society Committee regarding your Fixed Deposits'
                    email_from = settings.EMAIL_HOST_USER
                    recievers=[UserU.email]
                    send_mail( subject, message, email_from, recievers )
                    print("mail sent of fdcapital")
                userF.delete()
            return super(FDUpdate, self).post(request)


class LongLoanUpdate(UpdateView):
        model=Account
        form_class = LongLoanUpdateForm
        template_name = 'longloan_update_form.html'
        success_url=reverse_lazy('csadmin:loansadmin')

        def get_object(self):
            id_=self.kwargs.get("pk")
            UserA=Account.objects.get(pk=id_)
            print(UserA)
            return get_object_or_404(Account,pk=id_)

        def get_context_data(self, **kwargs):
            id_=self.kwargs.get("pk")
            UserA=Account.objects.get(pk=id_)
            context = super(UpdateView, self).get_context_data(**kwargs)
            longloandate=date.today()
            validate=False
            if (UserA.longloanbalance<=(UserA.longloanamount*50)/100):
                validate=True
            context={
                'Userid':UserA.username_id,
                'username':UserA.name,
                'islongloantaken':UserA.islongloantaken,
                'longloanadd':UserA.longloanadditional,
                'longloandt':longloandate,
                'longloanbal':UserA.longloanbalance,
                'validate':validate,
                'longloanamt':UserA.longloanamount,
                'longloanprd':UserA.longloanperiod,
            }
            return context

        def get_success_url(self):
            id_=self.kwargs.get("pk")
            UserA=Account.objects.get(pk=id_)
            UserU=User.objects.get(pk=UserA.username_id)
            print("Jd")
            print(UserA.islongloantaken)
            if (UserA.longloanbalance==0):
                UserA.islongloantaken=True
                UserA.longloanbalance=UserA.longloanamount
                longloanhistory(UserA.longloanamount,UserA.longloandate,UserA.longloanperiod,UserA.username)
            elif(UserA.longloanbalance!=0):
                UserA.longloanbalance=UserA.longloanbalance+UserA.longloanadditional
                UserA.longloanamount=UserA.longloanamount+UserA.longloanadditional
                longloanhistory(UserA.longloanadditional,date.today(),0,UserA.username)
                UserA.islongloantaken=True
                print("jatin")
            UserA.save()
            print("Long Loan Updated Mail")
            print(UserU.email)
            messages.success(self.request, 'Mail sent')
            message="Dear sir/ma'am your DJSCOE CS account " + str(UserA) + " Long Loan Amount is updated to " + str(UserA.longloanamount) + "for the period of" + str(UserA.longloanperiod)
            subject = 'This email is from Credit Society Committee'
            email_from = settings.EMAIL_HOST_USER
            recievers=[UserU.email]
            send_mail( subject, message, email_from, recievers )
            print("mail sent from suc for update in long loan")
            return reverse_lazy('csadmin:loansadmin')

class EmerLoanUpdate(UpdateView):
        model=Account
        form_class = EmerLoanUpdateForm
        template_name = 'emerloan_update_form.html'
        success_url=reverse_lazy('csadmin:loansadmin')

        def get_object(self):
            id_=self.kwargs.get("pk")
            UserA=Account.objects.get(pk=id_)
            print(UserA)
            return get_object_or_404(Account,pk=id_)

        def get_context_data(self, **kwargs):
            id_=self.kwargs.get("pk")
            UserA=Account.objects.get(pk=id_)
            context = super(UpdateView, self).get_context_data(**kwargs)
            emerloandate=date.today()
            print(UserA)
            print('Emergency Loan Upate')
            context={
                'Userid':UserA.username_id,
                'emerloanamt':UserA.emerloanamount,
                'emerloanprd':UserA.emerloanperiod,
                'isloanemertaken':UserA.isloanemertaken,
                'emerloandt':emerloandate,
                'username':UserA.name
            }
            return context

        def get_success_url(self):
            id_=self.kwargs.get("pk")
            UserA=Account.objects.get(pk=id_)
            UserU=User.objects.get(pk=UserA.username_id)
            print(UserU)
            if (UserA.emerloanbalance==0):
                UserA.isloanemertaken=True
                UserA.emerloanbalance=UserA.emerloanamount
                emerloanhistory(UserA.emerloanamount,UserA.emerloandate,UserA.emerloanperiod,UserA.username)
            UserA.save()
            print("Emergency loan updated mail")
            print(UserU.email)
            messages.success(self.request, 'Mail sent')
            message="Dear sir/ma'am your DJSCOE CS account " + str(UserA.name) + " Emergency Loan Amount is updated to " + str(UserA.emerloanamount) + " for the period of " + str(UserA.emerloanperiod)
            subject = 'This email is from Credit Society Committee'
            email_from = settings.EMAIL_HOST_USER
            recievers=[UserU.email]
            send_mail( subject, message, email_from, recievers)
            print("mail sent from suc for update in emer loan")
            return reverse_lazy('csadmin:loansadmin')

class SharesUpdate(UpdateView):
        model=Account
        form_class = ShareUpdateForm
        template_name = 'shares_update_form.html'
        success_url=reverse_lazy('csadmin:members')

        def get_object(self):
            id_=self.kwargs.get("pk")
            UserA=Account.objects.get(pk=id_)
            print(UserA)
            return get_object_or_404(Account,pk=id_)

        def get_context_data(self, **kwargs):
            id_=self.kwargs.get("pk")
            UserA=Account.objects.get(pk=id_)
            context = super(UpdateView, self).get_context_data(**kwargs)
            print(UserA)
            print('Shares Updated')
            context={
                'Userid':UserA.username_id,
                'usershare':UserA.sharevalue,
                'username':UserA.name,
            }
            return context

        def get_success_url(self):
            id_=self.kwargs.get("pk")
            UserA=Account.objects.get(pk=id_)
            UserU=User.objects.get(pk=UserA.username_id)
            print(UserU)
            if(UserA.shareamount==0):
                UserA.cdamount=UserA.sharevalue
            elif(UserA.cdamount==0):
                UserA.shareamount=UserA.sharevalue
            UserA.Noofshares=(UserA.sharevalue)/100
            UserA.save()
            print("shares updated mail")
            print(UserU.email)
            messages.success(self.request, 'Mail sent')
            message="Dear sir/ma'am your DJSCOE CS account " + str(UserA.name) + " Shares is updated to " + str(UserA.sharevalue)
            subject = 'This email is from Credit Society Committee'
            email_from = settings.EMAIL_HOST_USER
            recievers=[UserU.email]
            send_mail( subject, message, email_from, recievers )
            print("mail sent from suc for update in shares")
            # return get_object_or_404(User,id=id_)
            return reverse_lazy('csadmin:members')

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        template = get_template('tableview.html')
        accounts=Account.objects.all
        todaydate=date.today()
        month=["Janurary","Feburary","March","April","May","June","July","August","September","October","November","December"]
        pmonth=(date.today().month)-2
        prevmonth=month[pmonth]
        year=date.today().year
        context ={
            'year':year,
            'todaydate':todaydate,
            'prevmonth':prevmonth,
            'accounts':accounts,
        }
        html = template.render(context)
        pdf = render_to_pdf('tableview.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


# cron tak(scheduled tasks)
@cron_task(crontab="* * * * *")
def calcinvest():
    Members=Account.objects.all()
    Interests=interests.objects.all().last()
    #share parameters
    for i in  Members.iterator():
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
        i.save()

@cron_task(crontab="* * * * *")
def longloan():
    Members=Account.objects.all()
    Interests=interests.objects.all().last()
    #loan parameters
    Rate=Interests.longloaninterest
    R=Rate/(12*100) #rate of interest for each month

    for i in  Members.iterator():
        N=i.longloanperiod
        A=i.longloanamount
        if(N!=0):
            if(i.longloanprinciple==0 and i.longloaninterestamount==0):
                i.longloanemi=(A*R*(1+R)**N)/(((1+R)**N)-1)
                i.longloaninterestamount=R*A
                i.longloanprinciple=i.longloanemi-i.longloaninterestamount
                i.longloanbalance=i.longloanamount-i.longloanprinciple
            elif(i.longloanbalance<=i.longloanemi and i.longloanbalance!=0):
                i.longloanprinciple=i.longloanbalance
                i.longloaninterestamount=i.longloanemi-i.longloanprinciple
                i.longloanbalance=0
            elif(i.longloanbalance==0):
                i.longloanamount=0
                i.longloanbalance=0
                i.longloanperiod=0
                i.longloanemi=0
                i.longloaninterestamount=0
                i.longloanprinciple=0
                i.displaydownpayment=0
                i.islongloantaken=False
            else:
                i.longloanemi=(A*R*(1+R)**N)/(((1+R)**N)-1)
                i.longloaninterestamount=R*i.longloanbalance
                i.longloanprinciple=i.longloanemi-i.longloaninterestamount
                i.longloanbalance=i.longloanbalance-i.longloanprinciple
        i.save()


@cron_task(crontab="* * * * *")
def emergencyloan():
    Members=Account.objects.all()
    Interests=interests.objects.all().last()
    #Emergencyloan parameters
    Rate=Interests.emerloaninterest
    R=Rate/(12*100) #rate of interest for each month

    for i in  Members.iterator():
        N=i.emerloanperiod
        A=i.emerloanamount
        if(i.isloanemertaken==True):
            if(i.emerloanprinciple==0 and i.emerloaninterestamount==0):
                i.emerloanemi=(A*R*(1+R)**N)/(((1+R)**N)-1)
                i.emerloaninterestamount=R*A
                i.emerloanprinciple=i.emerloanemi-i.emerloaninterestamount
                i.emerloanbalance=i.emerloanamount-i.emerloanprinciple
                print("loop1")
            elif(i.emerloanbalance<=i.emerloanemi and i.emerloanbalance!=0):
                i.emerloanprinciple=i.emerloanbalance
                i.emerloaninterestamount=i.emerloanemi-i.emerloanprinciple
                i.emerloanbalance=0
                print("loop2")
            elif(i.emerloanbalance==0):
                i.emerloanamount=0
                i.emerloanbalance=0
                i.emerloanperiod=0
                i.emerloanemi=0
                i.emerloaninterestamount=0
                i.emerloanprinciple=0
                i.isloanemertaken=False
                print("loop3")
            else:
                i.emerloanemi=(A*R*(1+R)**N)/(((1+R)**N)-1)
                i.emerloaninterestamount=R*i.emerloanbalance
                i.emerloanprinciple=i.emerloanemi-i.emerloaninterestamount
                i.emerloanbalance=i.emerloanbalance-i.emerloanprinciple
                print("loop4")
        i.totalamount=i.shareamount+i.cdamount+i.emerloanprinciple+i.emerloaninterestamount+i.emerloanprinciple+i.emerloaninterestamount
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
