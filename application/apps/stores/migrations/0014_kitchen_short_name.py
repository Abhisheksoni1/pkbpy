# Generated by Django 2.1 on 2019-09-06 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0013_auto_20190905_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='kitchen',
            name='short_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
