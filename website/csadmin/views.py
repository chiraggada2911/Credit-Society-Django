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
from django.template.loader import get_template

#for date and time
import datetime
from dateutil import relativedelta

#forms
from django.forms import ModelForm
from csadmin.forms import ShareDividendForm,CDDividendForm,LongLoanForm,EmergencyLoanForm,FDInterestForm

# Create your views here.
def index(request):
    return render (request,'index.html')


@login_required
def commander(request):
    context={
        'dashb':"active"
    }
    return render (request,'console.html',context=context)

@login_required
def members(request):
    Members=Account.objects.all()
    Interests=interests.objects.all
    sharebalance = 0
    cdbalance = 0
    for i in  Members.iterator():
        date = i.dateofjoining
        datetoday=datetime.date.today()
        days=relativedelta.relativedelta(datetoday,date)
        nod=days.months
        year = days.years
        final = nod + 12 * year
        print("shareamount")
        print(i.shareamount)
        totalInvestment = final * (i.shareamount)
        if totalInvestment >= 5000:
            cdbalance = totalInvestment - 5000
            i.sharebalance = 5000
            i.cdbalance=cdbalance
            i.save()
            i.save()
        print(sharebalance)
        print(cdbalance)

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
    print(Interests)
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
                t=interests.objects.get(id=1)
                t.sharedividend=sharedividend
                t.save()
                print("valid_share+saved")
        elif 'btncd' in request.POST:
            tcddividend=CDDividendForm(request.POST)
            print("POST_2")
            if tcddividend.is_valid():
                cddividend = tcddividend.cleaned_data['fcddividend']
                t=interests.objects.get(id=1)
                t.cddividend=cddividend
                t.save()
                print("valid_cd")
        elif 'btnlongloan' in request.POST:
            tlongloaninterest=LongLoanForm(request.POST)
            print("POST_3")
            if tlongloaninterest.is_valid():
                longloaninterest = tlongloaninterest.cleaned_data['flongloaninterest']
                t=interests.objects.get(id=1)
                t.longloaninterest=longloaninterest
                t.save()
                print("valid_longloan")
        elif 'btnemerloan' in request.POST:
            temergencyloaninterest=EmergencyLoanForm(request.POST)
            print("POST_4")
            if temergencyloaninterest.is_valid():
                emergencyloaninterest = temergencyloaninterest.cleaned_data['femergencylaoninterest']
                t=interests.objects.get(id=1)
                t.emerloaninterest=emergencyloaninterest
                t.save()
                print("valid_emerloan")
        elif 'btnfd' in request.POST:
            tfdinterest=FDInterestForm(request.POST)
            print("POST_5")
            if tfdinterest.is_valid():
                fdinterest = tfdinterest.cleaned_data['ffdinterest']
                t=interests.objects.get(id=1)
                t.fdinterest=fdinterest
                t.save()
                print("valid_fd")

    context={
        'money':"active"
    }
    return render (request,'totalmoney.html',context=context)

#class adduseraccountform(ModelForm):
class UserCreate(CreateView):
        #model=User
        fields=['first_name','last_name','username','email','password']
        #make_password(password)
        success_url=reverse_lazy('csadmin:account_create')

class AccountCreate(CreateView):
        model=Account
        fields=['accountnumber','username','name','sapid','dateofjoining','shareamount','sharesstartingnumber','sharesendingnumber',]
        success_url=reverse_lazy('csadmin:members')

class FDUpdate(UpdateView):
        model=Account
        fields=['username','fdcapital','fdmaturitydate']
        success_url=reverse_lazy('csadmin:members')
        # 
        # def get_object(self):
        #     id_=self.kwargs.get("id")
        #     return get_object_or_404(id=id_)
        # def form_valid(self,form):
        #

class Loanadd(CreateView):
        model=Account
        fields=['username','isloantaken','longloanamount']
        success_url=reverse_lazy('csadmin:members')

class Sharesadd(CreateView):
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
