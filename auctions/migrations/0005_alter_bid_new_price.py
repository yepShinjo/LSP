# Generated by Django 4.1.1 on 2022-12-23 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_category_user_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='new_price',
            field=models.IntegerField(default=0),
        ),
    ]
