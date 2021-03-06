# Generated by Django 2.1 on 2019-05-29 06:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stores', '0008_kitchen_mobile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(blank=True, default='PERCENTAGE', max_length=50, null=True)),
                ('add_on', models.CharField(blank=True, default='CORE', max_length=50, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('description', models.TextField(blank=True, null=True)),
                ('terms_and_conditions', models.TextField(blank=True, null=True)),
                ('order_type', models.CharField(blank=True, default='DELIVERY', max_length=50, null=True)),
                ('max_discount', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('from_date', models.DateField(blank=True, null=True)),
                ('to_date', models.DateField(blank=True, null=True)),
                ('from_time', models.TimeField(blank=True, null=True)),
                ('to_time', models.TimeField(blank=True, null=True)),
                ('code', models.CharField(blank=True, max_length=20, null=True)),
                ('validate_on_code', models.BooleanField(default=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('updated_on', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'discounts',
            },
        ),
        migrations.CreateModel(
            name='DiscountOnItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discounts', related_query_name='discount', to='discounts.Discount')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discount_items', related_query_name='discount_item', to='stores.Item')),
            ],
            options={
                'db_table': 'discount_on_items',
            },
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('max_discount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('description', models.TextField(blank=True, null=True)),
                ('minimum_order', models.DecimalField(decimal_places=2, default='0', max_digits=7)),
                ('type', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default='0', max_digits=7)),
                ('image', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.BooleanField(default=1)),
                ('is_deleted', models.BooleanField(default=0)),
                ('created_on', models.DateTimeField(null=True)),
                ('updated_on', models.DateTimeField(null=True)),
                ('from_date', models.DateField(blank=True, null=True)),
                ('to_date', models.DateField(blank=True, null=True)),
                ('from_time', models.TimeField(blank=True, null=True)),
                ('to_time', models.TimeField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'promo_codes',
            },
        ),
    ]
