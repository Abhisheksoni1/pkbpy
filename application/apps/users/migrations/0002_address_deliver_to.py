# Generated by Django 2.1 on 2019-05-16 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='deliver_to',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
