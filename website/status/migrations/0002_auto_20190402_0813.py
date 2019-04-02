# Generated by Django 2.1.5 on 2019-04-02 02:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='Totalamount',
        ),
        migrations.AddField(
            model_name='account',
            name='cdinterest',
            field=models.IntegerField(blank=True, null=True),
        ),
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
        migrations.AddField(
            model_name='account',
            name='isloantaken',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='totalamount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='account',
            name='dividend',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='emerloanbalance',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='emerloanemi',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='emerloaninterest',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='emerloanprinciple',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='longloanbalance',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='longloanemi',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='longloaninterest',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='longloanprinciple',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='sharesendingnumber',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='sharesstartingnumber',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Login',
        ),
    ]
