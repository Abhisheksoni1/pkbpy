# Generated by Django 2.1 on 2019-05-31 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0008_kitchen_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='kitchen',
            name='delivery_charges',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
    ]