# Generated by Django 2.1 on 2019-09-09 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20190909_0937'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='payment_mode',
            new_name='purchase_method',
        ),
    ]
