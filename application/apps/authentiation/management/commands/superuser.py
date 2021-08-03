from django.contrib.auth.models import User, Group
from django.core.management import BaseCommand
from django.contrib.auth.management.commands import createsuperuser
class Command(createsuperuser.Command):
    help = 'Create Default Groups'

    # def add_arguments(self, parser):
    #     parser.add_argument('total', type=int, help='Indicates the number of users to be created')
    #
    #     # Optional argument
    #     parser.add_argument('-p', '--prefix', type=str, help='Define a username prefix', )

    def handle(self, *args, **options):
        _groups = ['Super admin', 'Manager', 'User']
        for group in _groups:
            Group.objects.create(name=group)
            self.stdout.write("%s group created " % group)
        super().handle(*args, **options)
        if options['verbosity'] >= 1:
            print(self.user_instance)
            group = Group.objects.get(name__exact="Super admin")
            group.user_set.add(self.user_instance)
        self.stdout.write("new command modify")