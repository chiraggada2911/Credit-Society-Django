from django.contrib import admin
from .models import Account,Loan,Shares,Department,FixedDeposits,Record,Month
# Register your models here.

admin.site.register(Account)
admin.site.register(Loan)
admin.site.register(Shares)
admin.site.register(Department)
admin.site.register(FixedDeposits)
admin.site.register(Record)
admin.site.register(Month)
