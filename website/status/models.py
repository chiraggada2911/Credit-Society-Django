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
    Noofshares=models.IntegerField(default=0,null=True)
    #schema for Loans
    islongloantaken=models.BooleanField(default=False)
    isloanemertaken=models.BooleanField(default=False)

# main amount , the loan taken
    longloandate=models.DateField(null=True,blank=True)
    longloanamount=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    longloanprinciple=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    longloanperiod=models.IntegerField(blank=True,null=True,default=0)
    longloaninterestamount=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    longloanbalance=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    longloanadditional=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
#emi=interest + principle
    longloanemi=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)

    #emergency loan
    emerloandate=models.DateField(null=True,blank=True)
    emerloanamount=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    emerloanprinciple=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    emerloanperiod=models.IntegerField(blank=True,null=True,default=0)
    emerloaninterestamount=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    emerloanbalance=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
#emi=interest + principle
    emerloanemi=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
#downpayment
    downpayment=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    displaydownpayment=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    #schema for fixed Deposits
    FDCount=models.IntegerField(default=0,null=False)

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
    year=models.CharField(default=0,max_length=50,null=True)

class Notification(models.Model):
    notimessage=models.CharField(default=0,max_length=50,null=True)
    notidate=models.DateField(null=False,default=datetime.date.today())
    seen=models.BooleanField(default=False)
    sender=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.sender)

class FixedDeposits(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE,null=True,unique=False)
    fdcapital=models.IntegerField(default=0,null=True)
    fddate=models.DateField(null=True,blank=True)
    fdmaturitydate=models.DateField(null=True,blank=True)
    fdnumber=models.CharField(default=0,max_length=50,null=True)

    def __str__(self):
        return str(self.username)

class HistorylongLoan(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE,null=True,unique=False)
    longloanamount=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    longloandate=models.DateField(null=True,blank=True)
    longloanperiod=models.IntegerField(blank=True,null=True,default=0)
#emi=interest + principle
    #emergency loan

    def __str__(self):
        return str(self.username)

class HistoryemerLoan(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE,null=True,unique=False)
    emerloanamount=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    emerloanperiod=models.IntegerField(blank=True,null=True,default=0)
    emerloandate=models.DateField(null=True,blank=True)

    def __str__(self):
        return str(self.username)

class HistoryFd(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE,null=True,unique=False)
    fdcapital=models.IntegerField(default=0,null=True)
    fddate=models.DateField(null=True,blank=True)
    fdmaturitydate=models.DateField(null=True,blank=True)
    fdnumber=models.CharField(default=0,max_length=50,null=True)

    def __str__(self):
        return str(self.username)

class sharemonth(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE,null=True,unique=False)
    jan=models.IntegerField(blank=True,null=True,default=0)
    feb=models.IntegerField(blank=True,null=True,default=0)
    mar=models.IntegerField(blank=True,null=True,default=0)
    apr=models.IntegerField(blank=True,null=True,default=0)
    may=models.IntegerField(blank=True,null=True,default=0)
    jun=models.IntegerField(blank=True,null=True,default=0)
    jul=models.IntegerField(blank=True,null=True,default=0)
    aug=models.IntegerField(blank=True,null=True,default=0)
    sep=models.IntegerField(blank=True,null=True,default=0)
    oct=models.IntegerField(blank=True,null=True,default=0)
    nov=models.IntegerField(blank=True,null=True,default=0)
    dec=models.IntegerField(blank=True,null=True,default=0)
    encode=models.CharField(max_length=20,blank=True,null=True,default=0)

    def __str__(self):
        return str(self.username)

class cdmonth(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE,null=True,unique=False)
    jan=models.IntegerField(blank=True,null=True,default=0)
    feb=models.IntegerField(blank=True,null=True,default=0)
    mar=models.IntegerField(blank=True,null=True,default=0)
    apr=models.IntegerField(blank=True,null=True,default=0)
    may=models.IntegerField(blank=True,null=True,default=0)
    jun=models.IntegerField(blank=True,null=True,default=0)
    jul=models.IntegerField(blank=True,null=True,default=0)
    aug=models.IntegerField(blank=True,null=True,default=0)
    sep=models.IntegerField(blank=True,null=True,default=0)
    oct=models.IntegerField(blank=True,null=True,default=0)
    nov=models.IntegerField(blank=True,null=True,default=0)
    dec=models.IntegerField(blank=True,null=True,default=0)
    encode=models.CharField(max_length=20,blank=True,null=True,default=0)

    def __str__(self):
        return str(self.username)

class year(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE,null=True,unique=False)
    s_encode=models.CharField(max_length=20,blank=True,null=True,default=0)
    cd_encode=models.CharField(max_length=20,blank=True,null=True,default=0)
    year=models.CharField(max_length=20,blank=True,null=True,default=0)