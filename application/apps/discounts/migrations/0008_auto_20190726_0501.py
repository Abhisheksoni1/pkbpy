# Generated by Django 2.1 on 2019-07-26 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0007_auto_20190619_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='code',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
