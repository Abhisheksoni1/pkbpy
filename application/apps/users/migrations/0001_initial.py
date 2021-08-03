# Generated by Django 2.1 on 2019-05-02 06:21

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('gender', models.CharField(blank=True, max_length=100, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('profile_pic', models.CharField(blank=True, max_length=200, null=True)),
                ('mobile', models.CharField(max_length=20)),
                ('login_otp', models.CharField(blank=True, max_length=6, null=True)),
                ('global_login_token', models.CharField(max_length=100, null=True)),
                ('password_reset_token', models.CharField(blank=True, max_length=255, null=True)),
                ('is_email_verified', models.PositiveSmallIntegerField(default=0)),
                ('is_mobile_verified', models.PositiveSmallIntegerField(default=0)),
                ('updated_on', models.DateTimeField(null=True)),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('created_by', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'auth_user',
                'permissions': (('view_user', 'Can view users.'), ('list_user', 'Can list users.'), ('add_user', 'Can add users.'), ('edit_user', 'Can edit users.'), ('delete_user', 'Can delete users.'), ('csv_for_user', 'Can download csv for users.')),
                'default_permissions': (),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.CharField(blank=True, max_length=200, null=True)),
                ('address_line1', models.CharField(blank=True, max_length=200, null=True)),
                ('address_line2', models.CharField(blank=True, max_length=200, null=True)),
                ('state', models.CharField(blank=True, max_length=200, null=True)),
                ('country', models.CharField(blank=True, max_length=200, null=True)),
                ('pincode', models.CharField(blank=True, max_length=200, null=True)),
                ('created_on', models.DateTimeField(null=True)),
                ('updated_on', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', related_query_name='address', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_address',
            },
        ),
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_ip', models.CharField(blank=True, max_length=40, null=True)),
                ('login_country', models.CharField(blank=True, max_length=60, null=True)),
                ('login_os', models.CharField(blank=True, max_length=30, null=True)),
                ('login_browser', models.CharField(blank=True, max_length=50, null=True)),
                ('login_platform', models.CharField(blank=True, max_length=40, null=True)),
                ('is_loggedin', models.BooleanField(default=False)),
                ('auth_token', models.TextField(blank=True, null=True)),
                ('device_token', models.TextField(blank=True, null=True)),
                ('login_time', models.DateTimeField()),
                ('logout_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(default=1)),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.PROTECT, related_name='login_logs', related_query_name='login_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_login_logs',
                'permissions': (('view_login_logs', 'Can view login logs.'), ('list_login_logs', 'Can list login logs.'), ('add_login_logs', 'Can add login logs.'), ('edit_login_logs', 'Can edit login logs.'), ('delete_login_logs', 'Can delete login logs.'), ('csv_for_login_logs', 'Can download csv for login logs.')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='LoginSessionManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('global_login_token', models.CharField(blank=True, max_length=100)),
                ('device_session_key', models.CharField(blank=True, max_length=60, null=True)),
                ('device_category', models.CharField(blank=True, max_length=10, null=True)),
                ('created_on', models.DateTimeField()),
                ('updated_on', models.DateTimeField()),
                ('status', models.PositiveSmallIntegerField(default=1)),
                ('device_info', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='users.LoginLog')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.PROTECT, related_name='login_sessions', related_query_name='login_sessions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_login_session_manager',
                'permissions': (('view_login_sessions', 'Can view login sessions.'), ('list_login_sessions', 'Can list login sessions.'), ('add_login_sessions', 'Can add login sessions.'), ('edit_login_sessions', 'Can edit login sessions.'), ('delete_login_sessions', 'Can delete login sessions.'), ('csv_for_login_sessions', 'Can download csv for login sessions.')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anniversary', models.DateField(blank=True, null=True)),
                ('preferences', models.CharField(blank=True, max_length=100, null=True)),
                ('created_on', models.DateTimeField(null=True)),
                ('updated_on', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
        migrations.CreateModel(
            name='UserWallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('validity', models.DateTimeField(blank=True, null=True)),
                ('created_on', models.DateTimeField(null=True)),
                ('updated_on', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_wallet',
            },
        ),
        migrations.CreateModel(
            name='UserWalletLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('validity', models.DateTimeField(blank=True, null=True)),
                ('wallet_log_for', models.CharField(blank=True, max_length=200, null=True)),
                ('is_credited', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(null=True)),
                ('updated_on', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='walletlogs', related_query_name='walletlog', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_wallet_log',
            },
        ),
    ]
