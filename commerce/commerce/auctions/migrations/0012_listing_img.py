# Generated by Django 3.2.5 on 2021-07-30 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_listing_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='img',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
