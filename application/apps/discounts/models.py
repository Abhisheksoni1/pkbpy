from django.db import models
from apps.users.models import User
from apps.stores.models import Item


# Create your models here.

class Discount(models.Model):
    """
    Discount model resources
    """

    # order type status
    ORDER_TYPE_PICKUP = 'PICK-UP'
    ORDER_TYPE_DELIVERY = 'DELIVERY'
    ORDER_TYPE_DINEIN = 'DINE-IN'

    # Tax value type
    DISCOUNT_AS_PERCENTAGE = 'PERCENTAGE'
    DISCOUNT_AS_FIXED = 'FIXED'

    # Add on
    ADD_ON_CORE = 'CORE'
    ADD_ON_TOTAL = 'TOTAL'

    title = models.CharField(null=True, blank=True, max_length=100)
    type = models.CharField(null=True, blank=True, default=DISCOUNT_AS_PERCENTAGE, max_length=50)
    add_on = models.CharField(null=True, blank=True, default=ADD_ON_CORE, max_length=50)
    amount = models.DecimalField(max_digits=7, decimal_places=2,null=True)
    description = models.TextField(null=True, blank=True)
    terms_and_conditions = models.TextField(null=True, blank=True)
    order_type = models.CharField(default=ORDER_TYPE_DELIVERY, null=True, blank=True, max_length=50)
    percentage = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    from_time = models.TimeField(null=True, blank=True)
    to_time = models.TimeField(null=True, blank=True)
    code = models.CharField(null=True, blank=True, max_length=20)
    validate_on_code = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True, blank=True)
    updated_on = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, db_constraint=False)

    class Meta:
        db_table = 'discounts'

    def __repr__(self):
        """
        Return object representation for developer
        :return: string
        """
        return '<Discount(id: %d, title: %s)>' % (self.id, self.title)


class DiscountOnItem(models.Model):
    """
       Discount on Item model: This model  has relationship between Discount Model and Item Model, means what Discount value is going to apply for an Item.
       It has Many To Many Relationship.
    """

    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='discounts',
                                 related_query_name='discount')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='discount_items',
                             related_query_name='discount_item')

    class Meta:
        db_table = 'discount_on_items'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '(<DiscountOnItem(DiscountTitle:%s, with Discount-value:%d, on Item:%s)>)' % (
            self.discount.title, self.discount.amount, self.item.name)


class PromoCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(null=True, blank=True, max_length=100)
    max_discount = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    description = models.TextField(null=True, blank=True)
    minimum_order = models.DecimalField(max_digits=7, decimal_places=2, default='0')
    type = models.CharField(null=True, blank=True, max_length=100)
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    percentage = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    image = models.CharField(null=True, blank=True, max_length=100)
    status = models.BooleanField(default=1)
    is_deleted = models.BooleanField(default=0)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    from_time = models.TimeField(null=True, blank=True)
    to_time = models.TimeField(null=True, blank=True)
    code = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        db_table = 'promo_codes'


class UserPromoCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='promo', related_query_name='promos')
    promo = models.ForeignKey(PromoCode, on_delete=models.CASCADE, related_name='user_promo',
                              related_query_name='user_promos')

    class Meta:
        db_table = 'user_promos'


class PromoCodeAttribute(models.Model):
    """
    Kitchen Attribute Model: This model keep attributes of kitchen as key=value format.  e.g Minimum Order=Rs. 99.00
    """
    key = models.CharField(blank=True, null=True, max_length=100)
    code = models.ForeignKey(PromoCode, on_delete=models.CASCADE, db_constraint=False, null=True,
                             related_name='attributes', related_query_name='attribute')
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, db_constraint=False, null=True)

    class Meta:
        db_table = 'promo_code_attributes'
