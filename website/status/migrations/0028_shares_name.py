# Generated by Django 2.1.5 on 2019-03-20 04:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0027_auto_20190319_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='shares',
            name='Name',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='status.Account'),
        ),
    ]