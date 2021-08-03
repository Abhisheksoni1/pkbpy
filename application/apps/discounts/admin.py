from django.contrib import admin
from apps.discounts.models import Discount, DiscountOnItem
# Register your models here.

admin.site.register(Discount)
admin.site.register(DiscountOnItem)