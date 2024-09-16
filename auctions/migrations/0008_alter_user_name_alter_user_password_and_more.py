# Generated by Django 5.0.1 on 2024-06-22 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auction_auction_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.TextField(null=True, unique=True),
        ),
    ]
