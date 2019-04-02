from django.shortcuts import render
#models
from status.models import Account
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template

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

#for changing the monthly monthlyDeduction which shld be in the multiple of Rs. 500
    Final_new_change =0
    if request.method=="POST":
        New_money_change = change_MoneyForm(request.POST)

        if New_money_change.is_valid():
            Final_new_change = New_money_change.cleaned_data['new_amount']

            subject = 'This guy wants to change his monthly deduction'
            message = Accountholder.name +" : "+str(Final_new_change)
            email_from = settings.EMAIL_HOST_USER

            recipient_list = ['jatinhdalvi@gmail.com','aashulikabra@gmail.com','champtem11@gmail.com']

            send_mail( subject, message, email_from, recipient_list )
            print("mail sent")

    else:
        New_money_change=change_MoneyForm()
    print(Final_new_change)

#calculating totalInvestment
    date = Accountholder.dateofjoining

    context={
    'name':name,
    'Accountholder':Accountholder,
    'date':date,
    'dashboard':"active",
    }

    return render(request,'dashboard.html',context=context)

#not using!!
@login_required
def graph(request):
        current_user_id=request.user.username
        Accountholder=Account.objects.filter(username__username__icontains=current_user_id).get()
        context={
            'Accountholder':Accountholder,
        }
        return render(request,'graph_test.html',context=context)


@login_required
def shares(request):

    current_user_id=request.user.username
    Accountholder=Account.objects.filter(username__username__icontains=current_user_id).get()
    context={
        'Accountholder':Accountholder,
        'share':"active",
    }

    return render (request,'shares.html',context=context)

@login_required
def fixedDeposits(request):

    current_user_id=request.user.username
    Accountholder=Account.objects.filter(username__username__icontains=current_user_id).get()

#conditional mail for maturity of FDs
    dateMaturity = Accountholder.fdmaturitydate
    datetoday=datetime.date.today()

    date_diff_fd = (relativedelta.relativedelta(dateMaturity,datetoday))

    print(dateMaturity)
    print(datetoday)
    print((date_diff_fd).months)
    print((date_diff_fd).days)
    print(date_diff_fd)

    if ((date_diff_fd).months==1 & (date_diff_fd).days==0):
        subject = 'FD is getting matured soon'
        message = "Dear sir/ma'am your DJSCOE CS FD is getting matured on " + Accountholder.fdmaturitydate + "what wolud you like to do? reply on this email or contact Admin"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['jatinhdalvi@gmail.com','aashulikabra@gmail.com','champtem11@gmail.com']
        send_mail( subject, message, email_from, recipient_list )
        print("mail sent for maturity if FD")

    context={
        'Accountholder':Accountholder,
        'fixed':"active",
    }
    return render (request,'fixedDeposits.html',context=context)

@login_required
def loanuser(request):

#Email for choice on request in taking loan
    if request.method=="POST":
        loanreq = LoanReqForm(request.POST)

        if loanreq.is_valid():

            subject = 'This guy wants a loan'
            message = Accountholder.name +" : "
            email_from = settings.EMAIL_HOST_USER

            recipient_list = ['jatinhdalvi@gmail.com','aashulikabra@gmail.com','champtem11@gmail.com']

            send_mail( subject, message, email_from, recipient_list )
            print("mail sent")


    current_user_id = request.user.username
    Accountholder=Account.objects.filter(username__username__icontains=current_user_id).get()
    context={
        'Accountholder':Accountholder,
        'loan':"active",
    }
    return render (request,'Loansuser.html',context=context)

@login_required
def Investment(request):
    current_user_id=request.user.username
    Accountholder=Account.objects.filter(username__username__icontains=current_user_id).get()
#calculates totalamount collected
    date = Accountholder.dateofjoining
    datetoday=datetime.date.today()
    days=relativedelta.relativedelta(datetoday,date)
    nod=days.months
    year = days.years
    final = nod + 12 * year
    print(Accountholder.shareamount)
    totalInvestment = final * (Accountholder.shareamount)
    context={
    'Accountholder':Accountholder,
    'totalInvestment':totalInvestment,
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
