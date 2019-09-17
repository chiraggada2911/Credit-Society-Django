from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
# models
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
from django.db.models.signals import post_save
from django.dispatch import receiver

#filter
from .filters import UserFilter

#for background tasks
from autotask.tasks import cron_task

#for date and time
from datetime import datetime,date
from dateutil import relativedelta

import datetime

#send_mail
from django.core.mail import send_mail
import smtplib

#forms
from django.forms import ModelForm
from csadmin.forms import AccountForm,NewUserForm,MessengerForm,SecretkeyForm,FDUpdateForm,ShareUpdateForm,LongLoanUpdateForm,EmerLoanUpdateForm,DownPaymentForm,AccountSearchForm,InterestsForm

# Create your views here.
def index(request):
    return render (request,'index.html')


@login_required
def index(request):
    Members=Account.objects.all()
    user_filter = UserFilter(request.GET, queryset=Members)
    context={
        'dashb':"active",
        'Members':Members,
        'filter': user_filter,
    }
    return render (request,'console.html',context=context)


@login_required
def members(request):
    Members=Account.objects.all()
    Interests=interests.objects.all().last()
    user_filter = UserFilter(request.GET, queryset=Members)
    context={
        'Members':Members,
        'Interests':Interests,
        'member':"active",
        'filter': user_filter,
    }
    return render (request,'members.html',context=context)


@login_required
def fixeddeposits(request):
    users=Account.objects.all()
    Interests=interests.objects.all().last()
    user_filter = UserFilter(request.GET, queryset=users)
    context={
        'fdadmin':users,
        'Interests':Interests,
        'Bank':"active",
        'filter': user_filter,
    }
    return render (request,'fd_admin.html',context=context)


@login_required
def loansadmin(request):
    Loansadmin=Account.objects.all()
    Interests=interests.objects.all().last()
    user_filter = UserFilter(request.GET, queryset=Loansadmin)
    context={
        'Loansadmin':Loansadmin,
        'Interests':Interests,
        'loan':"active",
        'filter': user_filter,
    }
    return render (request,'loans_admin.html',context=context)


@login_required
def change(request):

    Interest=interests.objects.all().last()
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
    }

    return render (request,'change.html',context=context)


@login_required
def message(request):
    recievers = []
    user=Account.objects.all
    users = User.objects.all()
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
            send_mail( subject, message, email_from, recievers )
            print("mail sent from messanger")

        else:
            print("error at validity of message")
    context={

        'message':"active",
    }
    return render (request,'messanger.html',context=context)


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

        # def get_success_url(self):
        #     Users=User.objects.all()
        #     message="interests rates changed"
        #     subject = 'This email is from Credit Society Committee'
        #     email_from = settings.EMAIL_HOST_USER
        #     recievers=[Users.email]
        #     send_mail( subject, message, email_from, recievers )
        #     return reverse_lazy('csadmin:members')

class AccountDelete(DeleteView):
    template_name = 'Userdelete.html'
    success_url=reverse_lazy('csadmin:members')

    def get_object(self):
        id_=self.kwargs.get("id")
        UserU=User.objects.get(id=id_)
        print(str(UserU) + " User is deleted")
        return get_object_or_404(User,id=id_)

    def get_success_url(self):
        id_=self.kwargs.get("id")
        UserU=User.objects.get(id=id_)
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
    Users=User.objects.all()
    context={
        'User':Users,
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
            UserA.save()
            return reverse_lazy('csadmin:fixeddeposits')

class FDUpdate(UpdateView):
        model=Account
        form_class = FDUpdateForm
        template_name = 'fixeddeposits_update_form.html'
        success_url=reverse_lazy('csadmin:fixeddeposits')

        def get_object(self):
            id_=self.kwargs.get("pk")
            UserA=Account.objects.get(pk=id_)
            print(UserA.name)
            return get_object_or_404(Account,pk=id_)

        def get_context_data(self, **kwargs):
            id_=self.kwargs.get("pk")
            UserA=Account.objects.get(pk=id_)
            context = super(UpdateView, self).get_context_data(**kwargs)
            print(UserA)
            print('FD update ')
            context={
                'Userid':UserA.username_id,
                'username':UserA.name,
                'userfddate':UserA.fdmaturitydate,
                'userfdamt':UserA.fdcapital,
            }
            return context

        def get_success_url(self):
            id_=self.kwargs.get("pk")
            UserA=Account.objects.get(pk=id_)
            UserU=User.objects.get(pk=UserA.username_id)
            print(UserU)
            print("FD updated Mail")
            print(UserU.email)
            message="Dear sir/ma'am your DJSCOE CS account " + str(UserA.name) + " Fixed Deposit Capital is updated to " + str(UserA.fdcapital)
            subject = 'This email is from Credit Society Committee'
            email_from = settings.EMAIL_HOST_USER
            recievers=[UserU.email]
            send_mail( subject, message, email_from, recievers )
            print("mail sent from suc for update in fdcapital")
            return reverse_lazy('csadmin:fixeddeposits')

        def post(self,request,**kwargs):
            id_=self.kwargs.get("pk")
            Members=Account.objects.get(pk=id_)
            Interests=interests.objects.all().last()
            datetoday=datetime.date.today()
            date_diff_fd = (relativedelta.relativedelta(Members.fdmaturitydate,datetoday))
            print("date")
            print(date_diff_fd)

            UserU=User.objects.get(pk=Members.username_id)
            # datetoday=datetime.date.today()
            if "renew_button" in request.POST:
                # date_diff_fd = (relativedelta.relativedelta(Members.fdmaturitydate,datetoday))
                print(Members.fdmaturitydate)
                print(type(Members.fdmaturitydate))
                # print(Members.fdmaturitydate.year + 1 )
                if (Members.fdmaturitydate.year%4==0 and Members.fdmaturitydate.year%100!=0 or Members.fdmaturitydate.year%400==0):
                    Members.fdmaturitydate=Members.fdmaturitydate + datetime.timedelta(days=366)
                    SimpleInterest=Members.fdcapital*Interests.fdinterest/100

                    Members.fdcapital=Members.fdcapital+SimpleInterest
                    message="Dear sir/ma'am your DJSCOE CS account" + str(Members.name) + "Fd is renew and New maturity date is" + str(Members.fdmaturitydate)
                    subject = 'This email is from Credit Society Committee'
                    email_from = settings.EMAIL_HOST_USER
                    recievers=[UserU.email]
                    send_mail( subject, message, email_from, recievers )
                    print("mail sent of fdcapital")
                else:
                    Members.fdmaturitydate=Members.fdmaturitydate + datetime.timedelta(days=365)
                    SimpleInterest=Members.fdcapital*Interests.fdinterest/100
                    Members.fdcapital=Members.fdcapital+SimpleInterest
                    Members.fdcapital=Members.fdcapital+SimpleInterest
                    message="Dear sir/ma'am your DJSCOE CS account" + str(Members.name) + "Fd is renew and New maturity date is" + str(Members.fdmaturitydate)
                    subject = 'This email is from Credit Society Committee'
                    email_from = settings.EMAIL_HOST_USER
                    recievers=[UserU.email]
                    send_mail( subject, message, email_from, recievers )
                    print("mail sent of fdcapital")
                Members.save()
                # print(date_diff_fd)

            if "clr_button" in request.POST:
                print("clear")
                if (date_diff_fd.months==-1 or date_diff_fd.days==-1 or date_diff_fd.years==-1):
                    SimpleInterest=Members.fdcapital*5/100
                    fd_totalpay=Members.fdcapital+SimpleInterest
                    print(fd_totalpay)
                    print("fd totalpay")
                    Members.fdcapital=0
                else:
                    SimpleInterest=Members.fdcapital*Interests.fdinterest/100
                    fd_totalpay=Members.fdcapital+SimpleInterest
                    print(fd_totalpay)
                    Members.fdcapital=0

                # Members.fdmaturitydate=0

                message="Dear sir/ma'am your DJSCOE CS account" + str(Members.name) + "Your total amount" + str(fd_totalpay)
                subject = 'This email is from Credit Society Committee'
                email_from = settings.EMAIL_HOST_USER
                recievers=[UserU.email]
                send_mail( subject, message, email_from, recievers )
                print("mail sent of fdcapital")

            Members.save()
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
            print(UserA)
            print('Long loan update')
            print(type(UserA.longloanamount))
            print(type(UserA.longloanperiod))
            context={
                'Userid':UserA.username_id,
                'username':UserA.name,
                'longloanamt':UserA.longloanamount,
                'longloanprd':UserA.longloanperiod,
            }
            return context

        def get_success_url(self):
            id_=self.kwargs.get("pk")
            UserA=Account.objects.get(pk=id_)
            UserU=User.objects.get(pk=UserA.username_id)
            print(UserU)
            print("Long Loan Updated Mail")
            print(UserU.email)
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
            print(UserA)
            print('Emergency Loan Upate')
            context={
                'Userid':UserA.username_id,
                'emerloanamt':UserA.emerloanamount,
                'emerloanprd':UserA.emerloanperiod,
                'username':UserA.name
            }
            return context

        def get_success_url(self):
            id_=self.kwargs.get("pk")
            UserA=Account.objects.get(pk=id_)
            UserU=User.objects.get(pk=UserA.username_id)
            print(UserU)
            print("Emergency loan updated mail")
            print(UserU.email)
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
            print("shares updated mail")
            print(UserU.email)
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
        context ={
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
        i.Noofshares=(i.sharevalue)/100
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
        print(N)
        print(A)
        if(N!=0):
            if(i.longloanbalance==0 and i.longloanprinciple==0):
                EMI=(A*R*(1+R)**N)/(((1+R)**N)-1)
                i.longloanemi=EMI
                interestamount=R*A
                print(interestamount)
                i.longloaninterestamount=interestamount
                print(interestamount)
                principle=i.longloanemi-interestamount
                i.longloanprinciple=principle
                print(principle)
                i.longloanbalance=i.longloanamount-i.longloanprinciple
                print(i.longloanbalance)
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
                i.islongloantaken=False
            else:
                EMI=(A*R*(1+R)**N)/(((1+R)**N)-1)
                print(EMI)
                i.longloanemi=EMI
                interestamount=R*i.longloanbalance
                i.longloaninterestamount=interestamount
                print(interestamount)
                principle=EMI-interestamount
                i.longloanprinciple=principle
                print(principle)
                i.longloanbalance=i.longloanbalance-principle
                print("jd is best")
                print(type(i.longloanbalance))
        i.save()


@cron_task(crontab="* * * * *")
def emergencyloan():
    Members=Account.objects.all()
    Interests=interests.objects.all().last()
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
            if(i.emerloanbalance==0 and i.emerloanprinciple==0):
                EMI=(A*R*(1+R)*N)/(((1+R)*N)-1)
                interestamount=R*A
                i.emerloaninterestamount=interestamount
                print(interestamount)
                principle=EMI-interestamount
                i.emerloanprinciple=principle
                print(principle)
                i.emerloanbalance=i.emerloanamount-principle
                print(i.emerloanbalance)

            elif(i.emerloanbalance==0):
                i.emerloanamount=0
                i.emerloanbalance=0
                i.emerloanperiod=0
                i.emerloaninterestamount=0
                i.emerloanprinciple=0
                i.isemerloantaken=False

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
