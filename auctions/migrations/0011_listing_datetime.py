# Generated by Django 3.2.5 on 2021-07-30 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_listing_current_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='datetime',
            field=models.CharField(max_length=69, null=True),
        ),
    ]
