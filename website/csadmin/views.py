from django.shortcuts import render,get_object_or_404
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
from django.db.models.signals import post_save
from django.dispatch import receiver
#convert string to dict
import ast
from decimal import Decimal


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
from csadmin.forms import NewUserForm,MessengerForm,SecretkeyForm,FDUpdateForm,ShareUpdateForm,LongLoanUpdateForm,EmerLoanUpdateForm

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
def UserDelete(request):
    Users=User.objects.all()
    context={
        'User':Users,
    }
    return render (request,'deleteuser.html',context=context)

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
def change(request):

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

                    return redirect('/csadmin/changeit')
                else:
                    print("Not Allow!!")

    context={

        'money':"active",
    }

    return render (request,'change.html',context=context)

@login_required
def changeit(request):

    Interests=interests.objects.all()
    obj = interests.objects.get(id=1)
    full_history = (obj.history.all()).order_by('-timestamp')
    for i in full_history:
        x=i.changes
        dict=ast.literal_eval(x)
        for i in dict:
            col_name=i
            print(type(col_name))
            y=dict[i]
            print(i)
            print(y)
            result = Decimal(y[0])
            print(col_name)
            if(col_name=="sharedividend"):
                x=interests(sharedividend=result)
                x.save()
            elif(col_name=="cddividend"):
                x=interests(cddividend=result)
                x.save()
            elif(col_name=="fdinterest"):
                x=interests(fdinterest=result)
                x.save()
            elif(col_name=="emerloaninterest"):
                x=interests(emerloaninterest=result)
                x.save()
            elif(col_name=="longloaninterest"):
                x=interests(longloaninterest=result)
                x.save()
    context={
        'money':"active",
        'full_history':full_history,
    }

    return render (request,'changeit.html',context=context)

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

#big problem here!!!!!!!  username_id
#deleting only deletes form account model and not from users so soething else need to be done here!!
class AccountDelete(DeleteView):
    template_name = 'Userdelete.html'
    success_url=reverse_lazy('csadmin:members')
    def get_object(self):
        id_=self.kwargs.get("id")
        Userd=User.objects.get(id=id_)
        print(Userd)
        print("This User is deleted")
        print(Userd.email)

        message="Dear sir/ma'am your DJSCOE CS account " + str(Userd) + "is deleted by admin"
        subject = 'This email is from Credit Society Committee'
        email_from = settings.EMAIL_HOST_USER
        recievers=[Userd.email]
        send_mail( subject, message, email_from, recievers )
        print("mail sent from deleteing account")
        return get_object_or_404(User,id=id_)

class InterestsUpdate(UpdateView):
        model=interests
        fields=['sharedividend','cddividend','fdinterest','emerloaninterest','longloaninterest']
        # interest=interests.objects.get(id=1)
        success_url=reverse_lazy('csadmin:members')

class AccountCreate(CreateView):
        model=Account
        template_name = 'AccountCreate.html'
        fields=['accountnumber','username','name','sapid','dateofjoining','sharevalue','sharesstartingnumber','sharesendingnumber',]
        success_url=reverse_lazy('csadmin:members')

class FDUpdate(UpdateView):
        model=Account
        form_class = FDUpdateForm
        template_name = 'fixeddeposits_update_form.html'
        success_url=reverse_lazy('csadmin:bank')

class LongLoanUpdate(UpdateView):
        model=Account
        form_class = LongLoanUpdateForm
        template_name = 'longloan_update_form.html'
        success_url=reverse_lazy('csadmin:loansadmin')

class EmerLoanUpdate(UpdateView):
        model=Account
        form_class = EmerLoanUpdateForm
        template_name = 'emerloan_update_form.html'
        success_url=reverse_lazy('csadmin:loansadmin')

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
            if(i.longloanbalance==0 and i.longloanprinciple==0):
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
            elif(i.longloanbalance==0):
                i.longloanamount=0
                i.longloanbalance=0
                i.longloanperiod=0
                i.longloaninterestamount=0
                i.longloanprinciple=0
                i.islongloantaken=False
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
                print("jd is best")
                print(type(i.longloanbalance))
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
