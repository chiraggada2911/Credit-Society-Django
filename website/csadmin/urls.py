from django.urls import path
from . import views

app_name='csadmin'
urlpatterns = [
    # /status
    path('', views.commander,name="commander"),
    path('members', views.members,name="members"),
    path('bank', views.bank,name="bank"),
    path('loansadmin', views.loansadmin,name="loansadmin"),
    path('change', views.change,name="change"),
    path('message', views.message,name="message"),
    
    path('usercreate', views.UserCreate.as_view(),name='user_create'),
    path('account/create/', views.AccountCreate.as_view(), name='account_create'),

    path('shareupdate/(?P<pk>)/', views.ShareUpdate.as_view(), name='Shares_Update'),
    path('cdupdate/(?P<pk>)/', views.CDUpdate.as_view(), name='CD_Update'),
    path('emerloanupdate/(?P<pk>)/', views.EmerLoanUpdate.as_view(), name='EmerLoan_Update'),
    path('longloanupdate/(?P<pk>)/', views.LongLoanUpdate.as_view(), name='LongLoan_Update'),
    path('fdintupdate/(?P<pk>)/', views.FDinterestUpdate.as_view(), name='FDint_Update'),

    path('FDupdate/(?P<pk>)/', views.FDUpdate.as_view(), name='fd_update'),
    path('Loanupdate/(?P<pk>)/', views.LoanUpdate.as_view(), name='loan_update'),
    path('Sharesupdate/(?P<pk>)/', views.SharesUpdate.as_view(), name='shares _update'),
    path('tableview',views.GeneratePdf.as_view(),name="GeneratePdf"),

]
