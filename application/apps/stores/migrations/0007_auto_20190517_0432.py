# Generated by Django 2.1 on 2019-05-17 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0006_auto_20190516_0819'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='is_outof_stack',
            new_name='is_outof_stock',
        ),
    ]