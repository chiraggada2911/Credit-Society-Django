from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name='csadmin'
urlpatterns = [
    # /status
    path('', views.commander,name="commander"),
    path('members', views.members,name="members"),
    path('bank', views.bank,name="bank"),
    path('loansadmin', views.loansadmin,name="loansadmin"),
    path('changeit', views.changeit,name="changeit"),
    path('change', views.change,name="change"),
    path('message', views.message,name="message"),

    path('userdelete', login_required(views.UserDelete),name='user_delete'),
    path('usercreate', login_required(views.UserCreate.as_view()),name='user_create'),
    path('account/create/', login_required(views.AccountCreate.as_view()), name='account_create'),

    path('interests/(?P<pk>)', login_required(views.InterestsUpdate.as_view()), name='interest_update'),

    path('<int:id>/delete/',login_required(views.AccountDelete.as_view()),name='User_Delete'),
    path('FDupdate/(?P<pk>)/', login_required(views.FDUpdate.as_view()), name='fd_update'),
    path('Loanupdate/(?P<pk>)/', login_required(views.LoanUpdate.as_view()), name='loan_update'),
    path('Sharesupdate/(?P<pk>)/', login_required(views.SharesUpdate.as_view()), name='shares _update'),
    path('tableview',login_required(views.GeneratePdf.as_view()),name="GeneratePdf"),

]
