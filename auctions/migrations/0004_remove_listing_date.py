# Generated by Django 3.2.5 on 2021-08-15 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210815_2315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='date',
        ),
    ]
