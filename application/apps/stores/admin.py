from django.contrib import admin

# Register your models here.
from django.contrib import admin
from apps.stores.models import Store, StoreAttribute ,StoreManager, StoreOwner, Kitchen, KitchenAttribute, Category, Item, ItemPrice
# Register your models here.

admin.site.register(Store)
admin.site.register(StoreAttribute)
admin.site.register(StoreManager)
admin.site.register(StoreOwner)
admin.site.register(Kitchen)
admin.site.register(KitchenAttribute)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(ItemPrice)


