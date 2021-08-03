from django.db import models
from django.conf import settings

from django.utils import timezone
# Create your models here.


class PaymentHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_payment_paytm', on_delete=models.CASCADE)
    ORDERID = models.CharField('ORDER ID', max_length=30)
    TXNDATE = models.DateTimeField('TXN DATE', default=timezone.now)
    TXNID = models.CharField(max_length=256, null=True)
    BANKTXNID = models.CharField(max_length=128, null=True, blank=True)
    BANKNAME = models.CharField('BANK NAME', max_length=50, null=True, blank=True)
    RESPCODE = models.IntegerField('RESP CODE')
    PAYMENTMODE = models.CharField('PAYMENT MODE', max_length=10, null=True, blank=True)
    CURRENCY = models.CharField('CURRENCY', max_length=4, null=True, blank=True)
    GATEWAYNAME = models.CharField("GATEWAY NAME", max_length=30, null=True, blank=True)
    MID = models.CharField(max_length=40)
    RESPMSG = models.TextField('RESP MSG', max_length=250)
    TXNAMOUNT = models.FloatField('TXN AMOUNT')
    STATUS = models.CharField('STATUS', max_length=12)

    class Meta:
        app_label = 'payment'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '<Payment(%s:%s,  GATEWAYNAME:%s, STATUS:%s>' % (
            self.ORDERID, self.TXNID, self.GATEWAYNAME, self.STATUS)