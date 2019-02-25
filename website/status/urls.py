from django.urls import path
from . import views

app_name='status'
urlpatterns = [
    # /status
    path('', views.index,name="index"),
    path('details',views.details,name="details"),
    path('custlogin',views.custlogin,name="custlogin"),
    path('shares',views.shares,name="shares"),
    path('fixedDeposits',views.fixedDeposits,name="fixedDeposits"),
    path('Loanuser',views.loanuser,name="loanuser"),
    path('MonthlyDeduction',views.MonthlyDeduction,name="MonthlyDeduction"),
    path('Investment',views.Investment,name="Investment"),
    path('mail',views.email,name="mail"),
    path('pdf',views.GeneratePdf.as_view(),name="GeneratePdf"),
    path('change',views.popup,name="popup"),





]
