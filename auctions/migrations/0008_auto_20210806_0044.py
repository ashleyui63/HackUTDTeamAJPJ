# Generated by Django 3.1.3 on 2021-08-06 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210804_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='file_path',
            field=models.ImageField(default='images/depositphotos_227725020-stock-illustration-image-available-icon-flat-vector.jpeg', upload_to='imgaes/', verbose_name=''),
        ),
    ]
