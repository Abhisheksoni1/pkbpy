# Generated by Django 2.1 on 2019-07-30 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20190729_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmodel',
            name='card_no',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='paymentmodel',
            name='date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='paymentmodel',
            name='year',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]