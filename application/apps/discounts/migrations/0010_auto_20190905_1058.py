# Generated by Django 2.1 on 2019-09-05 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0009_auto_20190905_0547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
