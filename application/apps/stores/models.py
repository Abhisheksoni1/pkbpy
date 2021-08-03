from django.contrib.gis.db import models
from apps.users.models import User


# from django.contrib.gis.geos import Point


class Store(models.Model):
    """
    Store model, Create New store resource
    """
    name = models.CharField(max_length=100)
    tag_line = models.TextField(null=True, blank=True)
    logo = models.CharField(null=True, blank=True, max_length=100)
    logo_thumb = models.CharField(null=True, blank=True, max_length=100)
    image = models.CharField(null=True, blank=True, max_length=100)
    image_thumb = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    location = models.PointField(srid=4326, max_length=40, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    opening_time = models.CharField(null=True, blank=True, max_length=100)
    closing_time = models.CharField(null=True, blank=True, max_length=100)
    minimum_order = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    cost_for_two = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    delivery_time = models.CharField(null=True, blank=True, max_length=100)
    tin_no = models.CharField(null=True, blank=True, max_length=100)
    status = models.BooleanField(default=True,verbose_name='is_open')
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, db_constraint=False, null=True)


    class Meta:
        db_table = 'stores'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '<Store(Store-name : %s)>' % (self.name)


class StoreOwner(models.Model):
    """
    Store Owner resource
    """
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='owners', related_query_name='owner')
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'store_owners'


class StoreManager(models.Model):
    """
    Store Manager resource
    """
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='managers', related_query_name='manager')
    manager = models.OneToOneField(User, on_delete=models.CASCADE)
    manager_p = models.CharField(max_length=32, blank=True, default='cft@12345')

    class Meta:
        db_table = 'store_managers'


class Kitchen(models.Model):
    """
    Kitchen model, Create New kitchen resource

    """
    name = models.CharField(max_length=100)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='kitchens', related_query_name='kitchen')
    tag_line = models.TextField(null=True, blank=True)
    logo = models.CharField(null=True, blank=True, max_length=100)
    logo_thumb = models.CharField(null=True, blank=True, max_length=100)
    image = models.CharField(null=True, blank=True, max_length=100)
    image_thumb = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    location = models.PointField(srid=4326, max_length=40, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    minimum_order = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    cost_for_two = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    delivery_time = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    status = models.BooleanField(default=True,verbose_name='is_open')
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, db_constraint=False, null=True)
    mobile = models.TextField(blank=True, null=True)
    delivery_charges = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    packing_charges = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    short_name = models.CharField(null=True,max_length=200,blank=True)
    cod_limit = models.DecimalField(max_digits=7, decimal_places=2, null=True)

    class Meta:
        db_table = 'kitchens'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '<Kitchen(kitchen-name : %s, under-store:%s>' % (self.name, self.store.name)

    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "kitchen-%s" % self.id

class KitchenManager(models.Model):
    """
    Store Manager resource
    """
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='managers', related_query_name='manager')
    manager = models.OneToOneField(User, on_delete=models.CASCADE,related_name='usermanagers', related_query_name='usermanager')
    manager_p = models.CharField(max_length=32, blank=True, default='cft@12345')

    class Meta:
        db_table = 'kitchen_managers'

class KitchenDelivery(models.Model):
    """
    Store Manager resource
    """
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='deliveries', related_query_name='delivery')
    deliver_boy = models.ForeignKey(User, on_delete=models.CASCADE)
    deliver_boy_p = models.CharField(max_length=32, blank=True, default='cft@12345')

    class Meta:
        db_table = 'delivery_boys'


class StoreAttribute(models.Model):
    """
    Store Attribute Model: This model keep attributes of store as key=value format.  e.g Minimum Order=Rs. 99.00
    """
    key = models.CharField(blank=True, null=True, max_length=100)
    value = models.CharField(blank=True, null=True, max_length=100)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, db_constraint=False, null=True,
                              related_name='attributes', related_query_name='attribute')
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, db_constraint=False, null=True)

    class Meta:
        db_table = 'store_attributes'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '<StoreAttribute(%s:%s,  under-store:%s>' % (self.key, self.value, self.store.name)


class KitchenAttribute(models.Model):
    """
    Kitchen Attribute Model: This model keep attributes of kitchen as key=value format.  e.g Minimum Order=Rs. 99.00
    """
    key = models.CharField(blank=True, null=True, max_length=100)
    value = models.CharField(blank=True, null=True, max_length=100)
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, db_constraint=False, null=True,
                                related_name='attributes', related_query_name='attribute')
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, db_constraint=False, null=True)

    class Meta:
        db_table = 'kitchen_attributes'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '<KitchenAttribute(%s:%s,  kitchen:%s, store:%s>' % (
            self.key, self.value, self.kitchen.name, self.kitchen.store.name)


class Category(models.Model):
    """
    Category Model: This resource keeps list of Food-catergory serve by particular Kitchen.
    """

    name = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='categories',
                                related_query_name='category')
    image = models.CharField(null=True, blank=True, max_length=100)
    image_thumb = models.CharField(null=True, blank=True, max_length=100)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, db_constraint=False, null=True)

    class Meta:
        db_table = 'categories'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '<Category(Name:%s,  kitchen:%s>' % (self.name, self.kitchen.name)


class Item(models.Model):
    """
    Item Model: This resource keeps list of Item serve in particular Category
    """
    name = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items', related_query_name='item')
    image = models.CharField(null=True, blank=True, max_length=100)
    image_thumb = models.CharField(null=True, blank=True, max_length=100)
    food_type = models.CharField(null=True, blank=True, max_length=100)  # It will contain food type, e.g veg or non-veg
    is_offer_active = models.BooleanField(default=True)
    is_variant = models.BooleanField(default=False)  # If it is True, Item has variant options e.g Half, full, Quarter
    base_price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    is_outof_stock = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, db_constraint=False, null=True)

    class Meta:
        db_table = 'items'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '<Item(Name:%s, under category:%s)>' % (self.name, self.category.name)


class ItemPrice(models.Model):
    """
    Item Attributes Model: This resources keeps store Item's attribute related price
    """
    quantity_type = models.CharField(null=True, blank=True, max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='itemprices', related_query_name='itemprice')
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, db_constraint=False, null=True)

    class Meta:
        db_table = 'item_prices'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '<ItemPrice(Item:%s, Item Price:%s)>' % (self.item.name, self.price)
