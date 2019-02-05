from django.shortcuts import render
from status.models import Account,Loan,FixedDeposits,Shares,User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

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

    context={
    'name':name,
    'fixedDeposits':fixedDeposits,
    'Accountholder':Accountholder,
    'loanuser':loanuser,
    'shares':shares,
    }

    return render(request,'dashboard.html',context=context)



@login_required
def shares(request):

    current_user_id=request.user.username
    shares=Shares.objects.filter(shareholdersName__username__icontains=current_user_id).get()

    context={
        'shares':shares,

    }

    return render (request,'shares.html',context=context)

@login_required
def fixedDeposits(request):

    current_user_id=request.user.username
    fixedDeposits=FixedDeposits.objects.filter(fdholdersName__username__icontains=current_user_id).get()

    context={
        'fixedDeposits':fixedDeposits,

    }
    return render (request,'fixedDeposits.html',context=context)

@login_required
def loanuser(request):

    current_user_id = request.user.username
    loanuser = Loan.objects.filter(loanGivenTo__username__icontains=current_user_id).get()

    context={
        'loanuser':loanuser,
    }
    return render (request,'Loansuser.html',context=context)


@login_required
def MonthlyDeduction(request):

    current_user_name=request.user.username
    MonthlyDeduction=Account.objects.filter(accountholder__username__icontains=current_user_name).get()

    context={
        'MonthlyDeduction':MonthlyDeduction,
        'current_user_name':current_user_name
    }
    return render (request,'MonthlyDeduction.html',)

@login_required
def Investment(request):

    return render (request,'investment.html')
