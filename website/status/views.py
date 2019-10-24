from django.shortcuts import render
#models
from status.models import Account,interests,Notification,FixedDeposits,HistorylongLoan,HistoryemerLoan,HistoryFd,year
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from django.contrib import messages
#forms
from status.forms import change_MoneyForm,LoanReqForm

#for date and time
import datetime
from dateutil import relativedelta

#for E-mail
from django.core.mail import send_mail
import smtplib

#for PDF
from status.utils import render_to_pdf

from csadmin import views

def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request,'status/error_404.html', data)

def notisave(notificationmessage,senderid):
    notification=Notification()
    notification.notimessage=notificationmessage
    notification.sender_id=senderid
    notification.save()


def custlogin(request):
    if request.user.is_staff:
        return redirect('/csadmin/')
    else:
        return redirect('/status/details')




def index(request):
    '''code for fetching any data from the models
    for embedding it into the html template
    to be called here and saved into variables and then
    pass it as the third parameter to the render Function
    '''

    #space left for fetcing data from the models and populating the teplates

    return render(request,'cards.html')

@login_required
def details(request):
    '''this view return the details of the logged in user '''

    current_user_id=request.user.username
    name=str(Account.name)
    Accountholder=Account.objects.filter(username__username__icontains=current_user_id).get()
    fdcount=FixedDeposits.objects.filter(username_id=Accountholder.id).count()
    Interests=interests.objects.all().last()


#for changing the monthly monthlyDeduction which shld be in the multiple of Rs. 500
    Final_new_change =0
    if request.method=="POST":
        New_money_change = change_MoneyForm(request.POST)

        if New_money_change.is_valid():
            Final_new_change = New_money_change.cleaned_data['new_amount']

            subject = 'This guy wants to change his monthly deduction'
            message = "Change Monthly Deduction of " + Accountholder.name +" to Rs."+str(Final_new_change)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['jatinhdalvi@gmail.com','aashulikabra@gmail.com','champtem11@gmail.com']
            messages.success(request, 'Mail sent')
            notisave(str(message),request.user.id)
            send_mail( subject, message, email_from, recipient_list )
            print("mail sent")

    else:
        New_money_change=change_MoneyForm()
    print(Final_new_change)

#calculating totalInvestment
    date = Accountholder.dateofjoining
    print("loan")
    context={
    'name':name,
    'Accountholder':Accountholder,
    'fdcount':fdcount,
    'date':date,
    'Interests':Interests,
    'dashboard':"active",
    }

    return render(request,'dashboard.html',context=context)

@login_required
def committee(request):
        context={
        'committee':"active",
        }
        return render(request,'committee.html',context=context)


@login_required
def shares(request):

    current_user_id=request.user.username
    Accountholder=Account.objects.filter(username__username__icontains=current_user_id).get()
    print("boo")
    print(Accountholder.id)
    context={
        'Accountholder':Accountholder,
        'share':"active",
    }

    return render (request,'shares.html',context=context)

@login_required
def fixedDeposits(request):

    current_user_id=request.user.username
    Accountholder=Account.objects.filter(username__username__icontains=current_user_id).get()
    userF=FixedDeposits.objects.filter(username_id=Accountholder.id)
    fdcount=FixedDeposits.objects.filter(username_id=Accountholder.id).count()
    print(fdcount)
    print("Upar")
    # userF=FixedDeposits.objects.filter(id__id__icontains=Accountholder.id).get()
    Interests=interests.objects.all().last()

    context={
        'Accountholder':Accountholder,
        'Interests':Interests,
        'fdcount':fdcount,
        'userF':userF,
        'fixed':"active",
    }
    return render (request,'fixedDeposits.html',context=context)

@login_required
def loanuser(request):
    current_user_id = request.user.username
    currentuserid=request.user.id
    Accountholder=Account.objects.filter(username__username__icontains=current_user_id).get()
    Longloans=HistorylongLoan.objects.filter(username=currentuserid)
    countlongloans=Longloans.count()
    Emerloans=HistoryemerLoan.objects.filter(username=currentuserid)
    countemerloans=Emerloans.count()
    print(countlongloans)
    print(countemerloans)
    print("just")
    print(current_user_id)
    type="success"
    eligibility=""

    if Accountholder.longloanbalance > Accountholder.longloanamount*50/100:
        print("Not eligible for loan")
        eligibility="No"
    else:
        print("eligible for loan")
        eligibility="Yes"

#Email for choice on request in taking loan
    if request.method=="POST":
        loanreq = LoanReqForm(request.POST)
        if loanreq.is_valid():
            Loan_Amount=str(loanreq.cleaned_data['loan_amount'])
            print(Loan_Amount)
            print(Accountholder.teachingstaff)
            loan_amount=int(Loan_Amount)
            print(loan_amount)
            if eligibility=="Yes":
                if Accountholder.teachingstaff==True and loan_amount <= 1200000 :
                    print(Loan_Amount)
                    Loan_Choice=loanreq.cleaned_data['loanChoice']
                    print(Loan_Choice)
                    subject = 'This guy wants a loan'
                    message = Accountholder.name +" has requested for "+ Loan_Choice +" of Rs "+Loan_Amount
                    email_from = settings.EMAIL_HOST_USER
                    type="success"
                    recipient_list = ['jatinhdalvi@gmail.com','aashulikabra@gmail.com','champtem11@gmail.com']
                    messages.success(request, 'Mail sent')
                    notisave(str(message),request.user.id)
                    send_mail( subject, message, email_from, recipient_list )
                    print("mail sent")
                elif Accountholder.nonteachingstaff==True and loan_amount <= 900000:
                    print(Loan_Amount)
                    Loan_Choice=loanreq.cleaned_data['loanChoice']
                    print(Loan_Choice)
                    subject = 'This guy wants a loan'
                    message = Accountholder.name +" has requested for "+ Loan_Choice +" of Rs "+Loan_Amount
                    email_from = settings.EMAIL_HOST_USER
                    type="success"
                    recipient_list = ['jatinhdalvi@gmail.com','aashulikabra@gmail.com','champtem11@gmail.com']
                    messages.success(request, 'Mail sent')
                    notisave(str(message),request.user.id)
                    send_mail( subject, message, email_from, recipient_list )
                    print("mail sent")

                else:
                    loanreq=LoanReqForm()
                    messages.error(request, 'Enter a valid amount')
                    type="danger"
            else:
                messages.error(request, 'pay 50% of loan first')
                type="danger"


    context={
        'Accountholder':Accountholder,
        'Emerloans':Emerloans,
        'Longloans':Longloans,
        'countlongloans':countlongloans,
        'countemerloans':countemerloans,
        'loan':"active",
        'type':type,
        'eligibility':eligibility,
    }
    return render (request,'Loansuser.html',context=context)

@login_required
def Investment(request):
    current_user_id = request.user.username
    Accountholder=Account.objects.filter(username__username__icontains=current_user_id).get()

    context={
    'Accountholder':Accountholder,
    'investment':"active",
    }
    return render (request,'Investment.html',context=context)

#use http response here it'll work
# for pdf stuff Using WeasyPrint

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        template = get_template('pdf.html')
        current_user_id=request.user.username
        Accountholder=Account.objects.filter(username__username__icontains=current_user_id).get()
        context ={
            'Accountholder':Accountholder,
        }
        html = template.render(context)
        pdf = render_to_pdf('pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
