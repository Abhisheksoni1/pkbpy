from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand
import csv
from django.conf import settings

from apps.feedback.models import KitchenFeedback
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
        with open(settings.BASE_DIR + '/PKBfeedback.csv', 'rt')as f:
            data = csv.reader(f)
            ratings = map(lambda i: i[0], filter(lambda i: i[0] != 'Rating', data))
            i = 1144
            for rating in ratings:
                print("ddsdfdfds ")
                KitchenFeedback.objects.create(kitchen_id=4, rating=rating, created_by_id=i)
                i += 10
