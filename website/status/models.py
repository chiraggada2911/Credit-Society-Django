from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.

class Account(models.Model):
    """This is the schema for the account of every staff member"""
    monthlyDeduction=models.IntegerField()
    corpus=models.IntegerField(default=0,blank=True)
    sapid=models.IntegerField(default=0)
    AccountNumber=models.IntegerField(default=0,primary_key=True)
    dividend=models.FloatField(null=True,blank=True)
    name=models.CharField(max_length=50,null=False,default='')
    accountholder=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=False)
    dateofjoining=models.DateField()

    def __str__(self):
        return str(self.accountholder)


class Shares(models.Model):
    '''this is the schema for the shares assigned to every member'''
    sharesStartingNumber=models.IntegerField()
    sharesEndingNumber=models.IntegerField()
    valueoftheshares=models.IntegerField()
    shareholdersName=models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=False)

    def __str__(self):
        return self.shareholdersName.username



class Loan(models.Model):
    '''this is the schema for the loans given to the member only of the credit society'''
    loanAmount=models.IntegerField()
    emi=models.IntegerField()
    repaymentDue=models.DateField()
    rateOfInterest=models.FloatField()
    isLoanTaken=models.BooleanField(default=False)
    loanGivenTo=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.loanGivenTo.username


class FixedDeposits(models.Model):
    '''this is the schema for the details of the FDS that the credit society invests in
    and also their return details '''
    fdCapital=models.IntegerField()
    rateOfInterest=models.FloatField()
    maturityDate=models.DateField()
    fdholdersName=models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return str(self.fdholdersName)

class Month(models.Model):
    monthfield=models.CharField(max_length=50,default='january')
    def __str__(self):
        return self.monthfield


class Record(models.Model):
    '''this is the schema for individual records of transactions '''
    monthName=models.ForeignKey(Month,on_delete=models.SET_NULL,null=True,blank=True)
