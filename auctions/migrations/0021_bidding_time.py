# Generated by Django 3.2.5 on 2021-08-17 12:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_alter_listing_current_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidding',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
