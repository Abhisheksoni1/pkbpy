from django.db import models
from apps.users.models import User
from apps.stores.models import Store,Kitchen


class ContactPage(models.Model):
    """
    Contact page information for App.
    """
    contact_address = models.TextField(blank=True, null=True)
    whatsapp_number = models.TextField(blank=True, null=True)
    timing = models.TextField(blank=True, null=True)
    paytm_number = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    status = models.BooleanField(default=1)
    is_deleted = models.BooleanField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, db_constraint=False)

    class Meta:
        db_table = 'contact_page'

    def __repr__(self):
        """
        Return object representation for developer
        :return: string
        """
        return '<ContactPage(id: %d)>' % (self.id)


class Faqs(models.Model):
    """
    Faqs resource model
    """

    question = models.TextField(null=True, blank=True)
    short_answer = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=1)
    is_deleted = models.BooleanField(default=0)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, db_constraint=False)

    class Meta:
        db_table = 'faqs'

    def __repr__(self):
        """
        Return object representation for developer
        :return: string
        """
        return '<Faqs(id: %d)>' % (self.id)


class Page(models.Model):
    """
    Page Resource Model, e.g About us/Privacy Policy

    """
    title = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    image = models.CharField(null=True, blank=True, max_length=100)
    status = models.BooleanField(default=1)
    is_deleted = models.BooleanField(default=0)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, db_constraint=False)

    class Meta:
        db_table = 'pages'

    def __repr__(self):
        """
        Return object representation for developer
        :return: string
        """
        return '<Page(Title: %s)>' % (self.title)


class PromoBanner(models.Model):
    """
    Promotional Banner Resource Model: For Particular Store

    """
    title = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    kitchen = models.ForeignKey(Kitchen, on_delete=models.PROTECT, null=True, db_constraint=False)
    image = models.CharField(null=True, blank=True, max_length=100)
    status = models.BooleanField(default=1)
    is_deleted = models.BooleanField(default=0)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, db_constraint=False)

    class Meta:
        db_table = 'promo_banners'

    def __repr__(self):
        """
        Return object representation for developer
        :return: string
        """
        return '<PromoBanner(Title: %s)>' % (self.title)


class FinancialYear(models.Model):
    """
    Financial Year Resource Model: For Particular Store

    It will use for to maintain yearly record of order, receipt etc.

    """
    financial_year = models.CharField(null=True, blank=True, max_length=100)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, db_constraint=False)

    class Meta:
        db_table = 'financial_year'

    def __repr__(self):
        """
        Return object representation for developer
        :return: string
        """
        return '<FinancialYear(Year: %s)>' % (self.financial_year)


class PushNotifications(models.Model):
    """
        Push Notification Resource Model:
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, db_constraint=False)
    title = models.CharField(null=True, blank=True, max_length=100)
    message = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    is_block = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)


    class Meta:
        db_table = 'push_notifications'

    def __repr__(self):
        """
        Return object representation for developer
        :return: string
        """
        return '<PushNotifications(title: %s)>' % (self.title)