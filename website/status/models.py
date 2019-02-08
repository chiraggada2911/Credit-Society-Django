from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.


class Department(models.Model):
    '''this is the schema for the department of the user entered'''
    deaprtmentname=models.CharField(max_length=100,blank=False,null=False)

    def __str__(self):
        return self.deaprtmentname

class Account(models.Model):
    """This is the schema for the account of every staff member"""
    monthlyDeduction=models.IntegerField()
    corpus=models.IntegerField()
    accountholder=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    dateofjoining=models.DateField()
    department=models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,blank=False,related_name='department')

    def __str__(self):
        return str(self.accountholder)


class Shares(models.Model):
    '''this is the schema for the shares assigned to every member'''
    sharesStartingNumber=models.IntegerField()
    sharesEndingNumber=models.IntegerField()
    valueoftheshares=models.IntegerField()
    shareholdersName=models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.shareholdersName.username

class Loan(models.Model):
    '''this is the schema for the loans given to the member only of the credit society'''
    loanAmount=models.IntegerField()
    emi=models.IntegerField()
    repaymentDue=models.DateField()
    rateOfInterest=models.FloatField()
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
