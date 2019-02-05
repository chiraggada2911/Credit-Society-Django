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
    path('account/create/', views.AccountCreate.as_view(), name='account_create')

]
