# Generated by Django 2.1 on 2019-09-05 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0008_auto_20190726_0501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
    ]
