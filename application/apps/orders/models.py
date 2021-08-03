from django.db import models
from apps.users.models import User, Address
from apps.stores.models import Kitchen
from pkbadmin.views import stores_views, kitchens_views
from apps.stores.models import Store, Kitchen, Category, Item


# Create your models here.

class Order(models.Model):
    """
    Order model managing all the order list from mobile app as well take order from web portal

    """
    ORDER_STATUS_PENDING = '0'
    ORDER_STATUS_CONFIRMED = '1'
    ORDER_STATUS_DELIVERED = '2'
    ORDER_STATUS_DECLINED = '3'

    user = models.ForeignKey(User, on_delete=models.PROTECT, db_constraint=False)
    order_no = models.CharField(max_length=20)
    financial_year = models.CharField(max_length=10, null=True)
    receipt_no = models.CharField(max_length=50, null=True)
    kitchen = models.ForeignKey(Kitchen, on_delete=models.PROTECT, db_constraint=False, related_name='orders',
                                related_query_name='order')
    order_payment_id = models.CharField(null=True, blank=True, max_length=32)
    purchase_method = models.CharField(null=True, blank=True, max_length=20)
    delivery_type = models.CharField(null=True, blank=True, max_length=20)
    delivery_on = models.CharField(null=True, blank=True, max_length=20)
    estimated_delivery_time = models.CharField(null=True, blank=True, max_length=40)
    offer_id = models.IntegerField(null=True, blank=True, default=False)
    points = models.DecimalField(max_digits=7, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
    packaging_charges = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    payable_price = models.DecimalField(max_digits=7, decimal_places=2)
    grand_total = models.DecimalField(max_digits=7, decimal_places=2)
    earn_points = models.DecimalField(max_digits=7, decimal_places=2)
    special_note = models.CharField(null=True, blank=True, max_length=200)
    delivery_address = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True)
    updated_on = models.DateTimeField(null=True, blank=True)
    order_notes = models.CharField(null=True, blank=True, max_length=200)
    # discount = models.DecimalField(max_digits=7, decimal_places=2)
    discount_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, db_constraint=False,
                                    related_name='discounts',
                                    related_query_name='discount')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, db_constraint=False,
                                   related_name='orderupdates',
                                   related_query_name='orderupdate')
    order_status = models.IntegerField(default=False)
    delivery_boy = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=True)
    total_discount = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    total_tax = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)


    class Meta:
        db_table = 'orders'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '<Orders(Order: %s)>' % (self.order_no)


class OrderItems(models.Model):
    """
    Order Items model: manage all  order items for particular Order

    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_constraint=True, related_name='orderitems',
                              related_query_name='orderitem')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, db_constraint=True)
    quantity_type = models.CharField(null=True, blank=True, max_length=50)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    tax_value = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    offer_id = models.IntegerField()
    created_on = models.DateTimeField(null=True, blank=True)
    updated_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'order_items'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '<OrderItems(OrderItems: %s)>' % (self.order)


class OrderLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_constraint=True,
                              related_name='orderlogs', related_query_name='orderlog')
    order_status = models.IntegerField(default=False)
    created_on = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, db_constraint=False,
                                   related_name='orderlogupdates',
                                   related_query_name='orderlogupdate')

    class Meta:
        db_table = 'order_logs'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '<OrderLogs(OrderLogs: %s)>' % (self.order.order_no)
