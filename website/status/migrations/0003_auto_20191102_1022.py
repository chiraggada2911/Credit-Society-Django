# Generated by Django 2.2 on 2019-11-02 04:52

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('status', '0002_auto_20191101_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharemonth',
            name='year',
            field=models.IntegerField(blank=True, default=2019, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notidate',
            field=models.DateField(default=datetime.date(2019, 11, 2)),
        ),
        migrations.AlterUniqueTogether(
            name='sharemonth',
            unique_together={('username', 'year')},
        ),
        migrations.RemoveField(
            model_name='sharemonth',
            name='encode',
        ),
    ]
