# Generated by Django 2.1 on 2019-08-21 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20190730_0548'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmodel',
            name='card_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='paymentmodel',
            name='card_type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='paymentmodel',
            name='card_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
