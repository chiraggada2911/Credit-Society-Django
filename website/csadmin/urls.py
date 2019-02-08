from django.urls import path
from . import views

app_name='csadmin'
urlpatterns = [
    # /status
    path('', views.commander,name="commander"),
    path('members', views.members,name="members"),
    path('bank', views.bank,name="bank"),
    path('loansadmin', views.loansadmin,name="loansadmin"),
    path('totalmoney', views.totalmoney,name="totalmoney"),
    path('user/create/', views.UserCreate.as_view(), name='user_create'),
    path('account/create/', views.AccountCreate.as_view(), name='account_create'),
    path('fd/add/', views.Fdadd.as_view(), name='fd_add'),
    path('loan/add/', views.Loanadd.as_view(), name='loan_add'),
    path('shares/add/', views.Sharesadd.as_view(), name='shares_add')

]
