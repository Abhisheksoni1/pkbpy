# Generated by Django 2.1 on 2019-05-27 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0007_auto_20190517_0432'),
    ]

    operations = [
        migrations.AddField(
            model_name='kitchen',
            name='mobile',
            field=models.TextField(blank=True, null=True),
        ),
    ]
