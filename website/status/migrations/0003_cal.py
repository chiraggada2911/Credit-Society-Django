# Generated by Django 2.2 on 2019-07-15 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0002_account_islongloantaken'),
    ]

    operations = [
        migrations.CreateModel(
            name='cal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sharedividend', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('cddividend', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('fdinterest', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('emerloaninterest', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('longloaninterest', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
            ],
        ),
    ]
