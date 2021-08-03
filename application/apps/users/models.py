from django.db import models
from django.contrib.auth.models import AbstractUser, Group, User
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.conf import settings
from config.settings import AUTH_USER_MODEL


class User(AbstractUser):
    """
    Extending Abstract User here

    """
    gender = models.CharField(null=True, blank=True, max_length=100)
    dob = models.DateField(blank=True, null=True)
    profile_pic = models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=20, unique=True)
    login_otp = models.CharField(null=True, blank=True, max_length=6)
    global_login_token = models.CharField(null=True, max_length=100)
    password_reset_token = models.CharField(max_length=255, null=True, blank=True)
    is_email_verified = models.PositiveSmallIntegerField(default=0)
    is_mobile_verified = models.PositiveSmallIntegerField(default=0)
    updated_on = models.DateTimeField(null=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, db_constraint=False)


    class Meta:
        db_table = 'auth_user'

        default_permissions = ()
        permissions = (
            # Users related permissions
            ('view_user', 'Can view users.'),
            ('list_user', 'Can list users.'),
            ('add_user', 'Can add users.'),
            ('edit_user', 'Can edit users.'),
            ('delete_user', 'Can delete users.'),
            ('csv_for_user', 'Can download csv for users.'),

            # More Permissions
        )

    REQUIRED_FIELDS = ['email']

    def __repr__(self):
        """
        Return object representation for developer
        :return: string
        """
        return '<User(id: %d, username: %s, email: %s, mobile: %s, first_name: %s, global_login_token: %s)>' % (
            self.id, self.username, self.email, self.mobile, self.first_name, self.global_login_token
        )

    @property
    def group_name(self):
        return self.groups.values_list('name', flat=True)


class OtpLog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(null=True, blank=True, max_length=6)

    class Meta:
        db_table = 'otp_user'


class VerifyOtp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(null=True, blank=True, max_length=12)
    otp = models.CharField(null=True, blank=True, max_length=6)

    class Meta:
        db_table = 'otp_verify'


class LoginLog(models.Model):
    """
    Log of all login
    """
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        db_constraint=False,
        related_query_name='login_logs',
        related_name='login_logs'
    )
    login_ip = models.CharField(max_length=40, null=True, blank=True)
    login_country = models.CharField(max_length=60, null=True, blank=True)
    login_os = models.CharField(max_length=30, null=True, blank=True)
    login_browser = models.CharField(max_length=50, null=True, blank=True)
    login_platform = models.CharField(max_length=40, null=True, blank=True)
    is_loggedin = models.BooleanField(default=False)
    auth_token = models.TextField(null=True, blank=True)
    device_token = models.TextField(null=True, blank=True)
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(default=1)

    class Meta:
        db_table = 'user_login_logs'

        default_permissions = ()
        permissions = (
            ('view_login_logs', 'Can view login logs.'),
            ('list_login_logs', 'Can list login logs.'),
            ('add_login_logs', 'Can add login logs.'),
            ('edit_login_logs', 'Can edit login logs.'),
            ('delete_login_logs', 'Can delete login logs.'),
            ('csv_for_login_logs', 'Can download csv for login logs.'),
        )

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '<LoginLog(id : %d, login_ip : %s, login_country : %s)>' % (self.id, self.login_ip, self.login_country)


class LoginSessionManager(models.Model):
    """
    Manage the user session to maintain the login across all devices
    """
    DEVICE_CATEGORY_WEB = 'Website'
    DEVICE_CATEGORY_ANDROID = 'Android'
    DEVICE_CATEGORY_IOS = 'IOS'
    DEVICE_CATEGORY_MOBILE = 'Mobile'

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        db_constraint=False,
        related_query_name='login_sessions',
        related_name='login_sessions'
    )
    global_login_token = models.CharField(max_length=100, blank=True)
    device_session_key = models.CharField(max_length=60, null=True, blank=True)
    device_category = models.CharField(max_length=10, null=True, blank=True)
    device_info = models.ForeignKey(LoginLog, on_delete=models.PROTECT, db_constraint=False, null=True)
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    status = models.PositiveSmallIntegerField(default=1)

    class Meta:
        db_table = 'user_login_session_manager'

        default_permissions = ()
        permissions = (
            ('view_login_sessions', 'Can view login sessions.'),
            ('list_login_sessions', 'Can list login sessions.'),
            ('add_login_sessions', 'Can add login sessions.'),
            ('edit_login_sessions', 'Can edit login sessions.'),
            ('delete_login_sessions', 'Can delete login sessions.'),
            ('csv_for_login_sessions', 'Can download csv for login sessions.'),
        )

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '<LoginSessionManager(id : %d, device_category : %s, unique_key : %s, web_session_key : %s)>' % (
            self.id, self.device_category, self.unique_key, self.web_session_key)


class Address(models.Model):
    """
    Manage User Address
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', related_query_name='address')
    deliver_to = models.CharField(max_length=200, null=True, blank=True)
    address_type = models.CharField(max_length=200, null=True, blank=True)
    house_number = models.CharField(max_length=32, null=True, blank=True)
    address_line1 = models.CharField(max_length=200, null=True, blank=True)
    address_line2 = models.CharField(max_length=200, null=True, blank=True)
    land_mark = models.CharField(max_length=64, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    pincode = models.CharField(max_length=200, null=True, blank=True)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=False)
    latitude = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.CharField(max_length=100, null=True, blank=True)
    save_as = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'user_address'


class UserProfile(models.Model):
    """
    Manage User Profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    anniversary = models.DateField(null=True, blank=True)
    preferences = models.CharField(null=True, blank=True, max_length=100)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_profile'


class UserWallet(models.Model):
    """
    Manage user wallet
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    validity = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_wallet'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '<UserWallet(id : %d, amount:%d)>' % (
            self.id, self.amount)


class UserWalletLog(models.Model):
    """
    Manage User wallet log
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='walletlogs', related_query_name='walletlog')
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    validity = models.DateTimeField(null=True, blank=True)
    wallet_log_for = models.CharField(max_length=200, null=True, blank=True)
    is_credited = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_wallet_log'

    def __repr__(self):
        """
        Return object representation for developers
        :return: string
        """
        return '<UserWalletLog(id : %d, )>' % (
            self.id,)


class PaymentModel(models.Model):
    """ Manage User Card details log"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_method',
                             related_query_name='payment_methods')
    card_no = models.CharField(null=True, blank=True,max_length=200)
    date = models.CharField(null=True, blank=True,max_length=100)
    year = models.CharField(null=True, blank=True,max_length=100)
    card_url = models.CharField(null=True,blank=True,max_length=200)
    card_name = models.CharField(null=True,blank=True,max_length=200)
    card_type = models.CharField(null=True, blank=True, max_length=200)
    card_holder_name = models.CharField(null=True,blank=True,max_length=200)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_card_log'
