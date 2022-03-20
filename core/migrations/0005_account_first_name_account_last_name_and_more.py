# Generated by Django 4.0.2 on 2022-03-06 16:45

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_account_date_joined_account_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='nationality',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
    ]