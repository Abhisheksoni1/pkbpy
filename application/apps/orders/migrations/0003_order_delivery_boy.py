# Generated by Django 2.1 on 2019-06-10 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20190502_0621'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_boy',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
