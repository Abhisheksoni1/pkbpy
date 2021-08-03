from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create Default Groups'

    # def add_arguments(self, parser):
    #     parser.add_argument('total', type=int, help='Indicates the number of users to be created')
    #
    #     # Optional argument
    #     parser.add_argument('-p', '--prefix', type=str, help='Define a username prefix', )

    def handle(self, *args, **kwargs):
        _groups=['Super admin', 'Manager','User']
        print("hello")
        for group in _groups:
            Group.objects.create(name=group)