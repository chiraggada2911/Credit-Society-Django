# Generated by Django 2.2 on 2019-10-10 05:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0020_auto_20191010_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixeddeposits',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]