# Generated by Django 2.1 on 2019-09-13 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20190821_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmodel',
            name='card_holder_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
