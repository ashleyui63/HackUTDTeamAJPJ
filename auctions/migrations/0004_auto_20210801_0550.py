# Generated by Django 3.1.3 on 2021-08-01 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210801_0444'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='username',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='watching',
            field=models.ManyToManyField(related_name='watchlists', to='auctions.Listing'),
        ),
    ]