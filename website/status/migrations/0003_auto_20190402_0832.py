# Generated by Django 2.1.5 on 2019-04-02 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0002_auto_20190402_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='fdcapital',
            field=models.IntegerField(default=True, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='fdinterest',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='fdmaturitydate',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]