from django.urls import path
from . import views

app_name='landingPage'

urlpatterns=[

    path('',views.home,name="home")
]
