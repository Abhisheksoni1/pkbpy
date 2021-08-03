from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from apps.users.models import User, UserProfile, UserWallet, UserWalletLog


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created and not instance.is_staff:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if not instance.is_staff:
        instance.userprofile.save()


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        UserWallet.objects.create(user=instance, amount=100, created_on=timezone.now())


@receiver(post_save, sender=User)
def save_user_wallet(sender, instance, **kwargs):
    if not instance.is_staff:
        instance.userwallet.save()


@receiver(post_save, sender=User)
def create_user_wallet_log(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        UserWalletLog.objects.create(user=instance, amount=100, wallet_log_for="New Register Gift",
                                     created_on=timezone.now())




