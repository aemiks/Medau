# Generated by Django 4.0.2 on 2022-03-20 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_privatechatroom_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privatechatroom',
            name='title',
            field=models.CharField(default='Private Chat', max_length=20),
        ),
    ]
