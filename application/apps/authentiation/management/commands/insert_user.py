from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand
import csv
from django.conf import settings

from apps.users.models import UserWallet, UserWalletLog
from libraries.Functions import generate_otp


class Command(BaseCommand):
    help = 'Insert existing user from excel sheet'

    # def add_arguments(self, parser):
    #     parser.add_argument('total', type=int, help='Indicates the number of users to be created')
    #
    #     # Optional argument
    #     parser.add_argument('-p', '--prefix', type=str, help='Define a username prefix', )

    def handle(self, *args, **kwargs):
        user_groups = 'User'
        # print(settings.BASE_DIR )
        with open(settings.BASE_DIR + '/PKBusersdata.csv', 'rt')as f:
            data = csv.reader(f)
            for i, row in enumerate(data):
                # ['K Chatterjee', '9312764712', 'Dec 31, 2018 | 20:45:56', '117']
                print(i, row)
                if i == 0:
                    pass
                else:
                    validated_data = {}
                    otp = generate_otp(4)
                    validated_data['username'] = row[1]
                    validated_data['mobile'] = row[1]
                    validated_data['name'] = row[0]
                    validated_data['password'] = make_password(otp)
                    validated_data['is_staff'] = False
                    validated_data['is_superuser'] = False
                    validated_data['is_mobile_verified'] = False
                    validated_data['login_otp'] = otp
                    user = get_user_model().objects.create(**validated_data)
                    group = Group.objects.get(name__exact="User")
                    group.user_set.add(user)
                    group.save()
                    user_wallet = UserWallet.objects.get(user=user)
                    user_wallet.amount = row[3]
                    user_wallet.save()
                    user_wallet_log = UserWalletLog.objects.get(user=user)
                    user_wallet_log.amount = row[3]
                    user_wallet_log.save()

