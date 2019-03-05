from django.shortcuts import render
from status.models import Account,Loan,FixedDeposits,Shares,User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template

#for date and time
import datetime
from dateutil import relativedelta

#for E-mail
from django.core.mail import send_mail
import smtplib

#for PDF
from status.utils import render_to_pdf

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
    name=str(Account.accountholder)
    shares=Shares.objects.filter(shareholdersName__username__icontains=current_user_id).get()
    fixedDeposits=FixedDeposits.objects.filter(fdholdersName__username__icontains=current_user_id).get()
    loanuser = Loan.objects.filter(loanGivenTo__username__icontains=current_user_id).get()
    Accountholder=Account.objects.filter(accountholder__username__icontains=current_user_id).get()

    date = Accountholder.dateofjoining
    datetoday=datetime.date.today()
    days=datetoday-date
    nod=(days).days
    totalInvestment = nod * (Accountholder.corpus)
    context={
    'name':name,
    'fixedDeposits':fixedDeposits,
    'Accountholder':Accountholder,
    'loanuser':loanuser,
    'shares':shares,
    'totalInvestment':totalInvestment,
    'date':date,
    'dashboard':"active",
    }

    return render(request,'dashboard.html',context=context)



@login_required
def shares(request):

    current_user_id=request.user.username
    shares=Shares.objects.filter(shareholdersName__username__icontains=current_user_id).get()

    context={
        'shares':shares,
        'share':"active",

    }

    return render (request,'shares.html',context=context)

@login_required
def fixedDeposits(request):

    current_user_id=request.user.username
    fixedDeposits=FixedDeposits.objects.filter(fdholdersName__username__icontains=current_user_id).get()

    context={
        'fixedDeposits':fixedDeposits,
        'fixed':"active",
    }
    return render (request,'fixedDeposits.html',context=context)

@login_required
def loanuser(request):

    current_user_id = request.user.username
    loanuser = Loan.objects.filter(loanGivenTo__username__icontains=current_user_id).get()

    context={
        'loanuser':loanuser,
        'loan':"active",
    }
    return render (request,'Loansuser.html',context=context)


@login_required
def MonthlyDeduction(request):

    current_user_name=request.user.username
    MonthlyDeduction=Account.objects.filter(accountholder__username__icontains=current_user_name).get()

    context={
        'MonthlyDeduction':MonthlyDeduction,
        'current_user_name':current_user_name,
        'Deduction':"active",

    }
    return render (request,'MonthlyDeduction.html',context=context)

@login_required
def Investment(request):
    current_user_id=request.user.username
    Accountholder=Account.objects.filter(accountholder__username__icontains=current_user_id).get()

    date = Accountholder.dateofjoining
    datetoday=datetime.date.today()
    days=relativedelta.relativedelta(datetoday,date)
    nod=days.months
    year = days.years
    final = nod + 12 * year
    print(Accountholder.monthlyDeduction)
    totalInvestment = final * (Accountholder.monthlyDeduction)
    context={
    'totalInvestment':totalInvestment,
    'investment':"active",
    }
    return render (request,'Investment.html',context=context)

#use http response here it'll work
# for pdf stuff Using WeasyPrint
def email(request):
        subject = 'Thank you for registering to our site'
        message = ' it  means a world to us '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['jatinhdalvi@gmail.com','aashulikabra@gmail.com','champtem11@gmail.com']
        #send_mail( subject, message, email_from, recipient_list )
        print("mail sent")
        return render(request,'changemd.html')

#       def changemd(request):


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        template = get_template('pdf.html')

        context = {
            'today': datetime.date.today(),
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        html = template.render(context)
        pdf = render_to_pdf('pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

@login_required
def popup(request):
    if request.method == ["POST"]:
        a = request.POST['userInput']
        print (a)
    #newMonthlyDeduction = request.POST['userInput']

    return render(request,'email_popup.html')
