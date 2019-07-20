from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.
class Account(models.Model):
    #schema for data to show
    accountnumber=models.IntegerField(null=False,unique=True)
    username=models.ForeignKey(User,on_delete=models.CASCADE,null=True,unique=True)
    name=models.CharField(max_length=50,null=False)
    sapid=models.IntegerField(null=False,unique=True)
    dateofjoining=models.DateField(null=False)
    sharevalue=models.IntegerField(default=0,null=False)
    totalinvestment=models.IntegerField(default=0,null=False)
    shareamount=models.IntegerField(default=0,null=False)
    sharebalance=models.IntegerField(default=0)

    cdamount=models.IntegerField(default=0)
    cdbalance=models.IntegerField(default=0)
    #cdbalance + sharebalance = total investment
    totalamount=models.DecimalField(default=0,max_digits=10,decimal_places=2)
    #schema for shares
    Noofshares=models.IntegerField(null=True)
    #schema for Loans
    islongloantaken=models.BooleanField(default=False)
    isloanemertaken=models.BooleanField(default=False)
# main amount , the loan taken
    longloanamount=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    longloanprinciple=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    longloanperiod=models.IntegerField(blank=True,null=True,default=0)
    longloaninterestamount=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    longloanbalance=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
#emi=interest + principle
    longloanemi=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    #emergency loan
    emerloanamount=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    emerloanprinciple=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    emerloanperiod=models.IntegerField(blank=True,null=True,default=0)
    emerloaninterestamount=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    emerloanbalance=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
#emi=interest + principle
    emerloanemi=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    #schema for fixed Deposits
    fdcapital=models.IntegerField(default=0,null=True)
    fdmaturitydate=models.DateField(null=True)
    #teaching and nonteaching staff
    teachingstaff=models.BooleanField(default=False)
    nonteachingstaff=models.BooleanField(default=False)


    def __str__(self):
        return str(self.username)

class interests(models.Model):
    sharedividend=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    cddividend=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    fdinterest=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    emerloaninterest=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    longloaninterest=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    year=models.IntegerField(default=0,null=True)
