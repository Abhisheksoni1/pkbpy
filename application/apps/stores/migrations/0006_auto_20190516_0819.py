# Generated by Django 2.1 on 2019-05-16 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0005_auto_20190516_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='status',
            field=models.BooleanField(default=True, verbose_name='is_open'),
        ),
    ]
