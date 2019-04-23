import string

from django.contrib.auth.models import User
from status.models import interests
from django.utils.crypto import get_random_string
from celery.schedules import crontab

from celery import shared_task

@shared_task
def add(a,b):
    
    return(a)
