# Generated by Django 3.2.5 on 2021-07-28 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('FASHION', 'Fashion'), ('TECHNOLOGY', 'Technology'), ('SPORTS', 'Sports'), ('TOYS', 'Toys'), ('BOOKS', 'Books'), ('MUSIC', 'Music'), ('OTHER', 'Other')], max_length=69, null=True),
        ),
    ]
