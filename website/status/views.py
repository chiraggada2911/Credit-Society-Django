from django.shortcuts import render
from status.models import Account,Loan,FixedDeposits,Shares,User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
import datetime
from django.core.mail import send_mail
from django.conf import settings

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
    days=datetoday-date
    nod=(days).days
    totalInvestment = nod * (Accountholder.corpus)
    context={
    'totalInvestment':totalInvestment,
    'investment':"active",
    }
    return render (request,'Investment.html',context=context)

def email(request):

    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['aashulikabra@gmail.com',]
    send_mail( subject, message, email_from, recipient_list )

    return redirect(request,'investment.html')
