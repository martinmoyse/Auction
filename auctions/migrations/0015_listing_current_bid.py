# Generated by Django 3.2.5 on 2021-08-16 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_rename_bid_listing_starting_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='current_bid',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=11),
        ),
    ]
