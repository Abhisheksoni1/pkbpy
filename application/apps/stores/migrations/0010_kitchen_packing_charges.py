# Generated by Django 2.1 on 2019-06-18 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0009_kitchen_delivery_charges'),
    ]

    operations = [
        migrations.AddField(
            model_name='kitchen',
            name='packing_charges',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
    ]
