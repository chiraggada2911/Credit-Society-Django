# Generated by Django 2.2 on 2019-07-17 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0003_delete_cal'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='nonteachingstaff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='teachingstaff',
            field=models.BooleanField(default=False),
        ),
    ]
