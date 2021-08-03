# Generated by Django 2.1 on 2019-05-15 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_auto_20190502_0621'),
    ]

    operations = [
        migrations.AddField(
            model_name='kitchen',
            name='closing_time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='kitchen',
            name='cost_for_two',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='kitchen',
            name='delivery_time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='kitchen',
            name='minimum_order',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='kitchen',
            name='opening_time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='closing_time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='opening_time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
