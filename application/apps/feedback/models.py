from django.contrib.gis.db import models
from apps.users.models import User
from apps.stores.models import Store, Kitchen, Item
from apps.orders.models import Order


class KitchenFeedback(models.Model):
    """
    Kitchen Feedback model, Feedback from user-end for Kitchen
    """
    kitchen = models.ForeignKey(Kitchen, on_delete=models.PROTECT, db_constraint=False, null=True,
                                related_name='kitchenfeedbacks', related_query_name='kitchenfeedback')
    message = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    rating = models.FloatField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, db_constraint=False, null=True)

    class Meta:
        unique_together = (('kitchen', 'created_by'))
        db_table = 'kitchen_feedbacks'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '<KitchenFeedback(Feedback For: %s)>' % (self.kitchen.name)


class OrderFeedback(models.Model):
    """
    Order Feedback model, Feedback from user's end for particular Order
    """
    order = models.OneToOneField(Order, on_delete=models.PROTECT, db_constraint=False, null=True)
    message = models.TextField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, db_constraint=False, null=True)

    class Meta:
        db_table = 'order_feedbacks'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '<orderFeedback(Feedback For: %s)>' % (self.order.order_no)


class ItemFeedback(models.Model):
    """
    Item Feedback model, Feedback from user-end for Order Item.
    """
    feedback = models.ForeignKey(OrderFeedback, on_delete=models.PROTECT, db_constraint=False, null=True,
                                related_name='itemfeedbacks', related_query_name='itemfeedback')

    item=models.ForeignKey(Item, on_delete=models.PROTECT, db_constraint=False, null=True,
                                related_name='itemratings', related_query_name='itemrating')

    message = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    rating = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, db_constraint=False, null=True)

    class Meta:
        db_table = 'item_feedbacks'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '<ItemFeedback(Feedback For: %s)>' % (self.item.name)
