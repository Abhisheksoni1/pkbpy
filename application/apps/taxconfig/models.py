from django.db import models
from apps.users.models import User
from apps.stores.models import Item, ItemPrice


# Create your models here.

class Taxconfig(models.Model):
    """
    Tax model: This model store basic tax(s) information, e.g. title, value type
    """
    # Tax type status
    TAX_TYPE_FORWARD = 'FORWARD'
    TAX_TYPE_BACKWARD = 'BACKWARD'
    TAX_TYPE_CALCULATE = 'CALCULATE ON TAX'

    # order type status
    ORDER_TYPE_PICKUP = 'PICK-UP'
    ORDER_TYPE_DELIVERY = 'DELIVERY'
    ORDER_TYPE_DINE_IN = 'DINE-IN'

    # Tax value type
    TAX_AS_PERCENTAGE = 'PERCENTAGE'
    TAX_AS_FIXED = 'FIXED'

    title = models.CharField(null=True, blank=True, max_length=100)
    tax_type = models.CharField(default=TAX_TYPE_FORWARD, null=True, blank=True, max_length=100)
    order_type = models.CharField(default=ORDER_TYPE_DELIVERY, null=True, blank=True, max_length=100)
    value_type = models.CharField(default=TAX_AS_PERCENTAGE, max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    is_block = models.BooleanField(default=0)
    is_deleted = models.BooleanField(default=0)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, db_constraint=False, null=True)

    class Meta:
        db_table = 'taxes'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '(<Taxconfig(Title:%s,)>)' % (self.title)


class TaxOnItem(models.Model):
    """
       Tax on Item model: This model  has relationship between Tax Model and Item Model, means what tax value is going to apply for an Item.
       It has Many To Many Relationship.
    """

    tax = models.ForeignKey(Taxconfig, on_delete=models.CASCADE, related_name='taxes', related_query_name='tax')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_taxes', related_query_name='item_tax')

    class Meta:
        db_table = 'tax_on_items'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '(<TaxOnItem(TaxTitle:%s, with Tax-value:%.2f, on Item:%s)>)' % (
        self.tax.title, self.tax.amount, self.item.name)
