# Generated by Django 2.0.2 on 2018-10-31 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery_store', '0002_auto_20181028_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='descript',
            field=models.CharField(default='', max_length=10000000),
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='user',
            name='birth_day',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='product',
            name='available_quantity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(),
        ),
    ]