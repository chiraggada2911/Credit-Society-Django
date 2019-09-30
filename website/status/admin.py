from django.contrib import admin
from .models import Account,interests,Notification,FixedDeposits
# Register your models here.

admin.site.register(Account)
admin.site.register(interests)
admin.site.register(Notification)
admin.site.register(FixedDeposits)
