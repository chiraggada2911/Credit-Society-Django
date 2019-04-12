from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.
class Account(models.Model):
    #schema for data to show
    accountnumber=models.IntegerField(null=False,unique=True)
    username=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,unique=True)
    name=models.CharField(max_length=50,null=False)
    sapid=models.IntegerField(null=False,unique=True)
    dateofjoining=models.DateField(null=False)

    shareamount=models.IntegerField(default=0,null=False)
    sharebalance=models.IntegerField(default=0)

    cdamount=models.IntegerField(default=0)
    cdbalance=models.IntegerField(default=0)
    #cd + share = total amount
    totalamount=models.IntegerField(default=0)
    #schema for shares
    sharesstartingnumber=models.IntegerField(null=True)
    sharesendingnumber=models.IntegerField(null=True)
    #schema for Loans
    isloantaken=models.BooleanField(default=False)
# main amount , the loan taken
    longloanamount=models.IntegerField(blank=True,null=True)
    longloanprinciple=models.IntegerField(blank=True,null=True)

    longloaninterestamount=models.IntegerField(blank=True,null=True)
    longloanbalance=models.IntegerField(blank=True,null=True)
#emi=interest + principle
    longloanemi=models.IntegerField(blank=True,null=True)
    #emergency loan
    emerloanamount=models.IntegerField(blank=True,null=True)
    emerloanprinciple=models.IntegerField(blank=True,null=True)
    emerloaninterestamount=models.IntegerField(blank=True,null=True)
    emerloanbalance=models.IntegerField(blank=True,null=True)
#emi=interest + principle
    emerloanemi=models.IntegerField(blank=True,null=True)
    #schema for fixed Deposits
    fdcapital=models.IntegerField(default=True,null=True)
    fdmaturitydate=models.DateField(null=True)


    def __str__(self):
        return str(self.username)

class interests(models.Model):
    sharedividend=models.FloatField(blank=True,null=True)
    cddividend=models.FloatField(blank=True,null=True)
    fdinterest=models.FloatField(blank=True,null=True)
    emerloaninterest=models.FloatField(blank=True,null=True)
    longloaninterest=models.FloatField(blank=True,null=True)
