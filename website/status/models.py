from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.
class Account(models.Model):
    #schema for data to show
    accountnumber=models.IntegerField(null=False)
    username=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=50,null=False)
    sapid=models.IntegerField(null=False)
    dateofjoining=models.DateField(null=False)
    shareamount=models.IntegerField(default=0,null=False)
    sharebalance=models.IntegerField(default=0)
    cdamount=models.IntegerField(default=0)
    dividend=models.FloatField(null=True)
    cdbalance=models.IntegerField(default=0)
    cdinterest=models.IntegerField(blank=True,null=True)
    totalamount=models.IntegerField(default=0)
    #schema for shares
    sharesstartingnumber=models.IntegerField(null=True)
    sharesendingnumber=models.IntegerField(null=True)
    #schema for Loans
    isloantaken=models.BooleanField(default=False)
    longloanprinciple=models.IntegerField(blank=True,null=True)
    longloaninterest=models.IntegerField(blank=True,null=True)
    longloanbalance=models.IntegerField(blank=True,null=True)
    longloanemi=models.IntegerField(blank=True,null=True)
    emerloanprinciple=models.IntegerField(blank=True,null=True)
    emerloaninterest=models.IntegerField(blank=True,null=True)
    emerloanbalance=models.IntegerField(blank=True,null=True)
    emerloanemi=models.IntegerField(blank=True,null=True)
    #schema for fixed Deposits
    fdcapital=models.IntegerField(default=True,null=True)
    fdmaturitydate=models.IntegerField(blank=True,null=True)
    fdinterest=models.IntegerField(blank=True,null=True)
    

    def __str__(self):
        return str(self.username)
