# Generated by Django 2.1 on 2019-10-09 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0021_auto_20191009_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kitchenmanager',
            name='manager',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='usermanagers', related_query_name='usermanager', to=settings.AUTH_USER_MODEL),
        ),
    ]
