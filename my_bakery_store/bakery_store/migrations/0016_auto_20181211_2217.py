# Generated by Django 2.1.3 on 2018-12-11 15:17

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bakery_store', '0015_auto_20181208_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppliedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='event_id',
            field=models.CharField(default=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False), max_length=10, unique=True),
        ),
        migrations.AddField(
            model_name='event',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='appliedproduct',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bakery_store.Event'),
        ),
        migrations.AddField(
            model_name='appliedproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bakery_store.Product'),
        ),
    ]
