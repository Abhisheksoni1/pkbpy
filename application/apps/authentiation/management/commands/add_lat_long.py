from django.core.management.base import BaseCommand
from config import settings
import csv
from apps.stores.models import Store, Kitchen
from django.contrib.gis.geos import Point


class Command(BaseCommand):
    help = 'Create Default Groups'

    # def add_arguments(self, parser):
    #     parser.add_argument('total', type=int, help='Indicates the number of users to be created')
    #
    #     # Optional argument
    #     parser.add_argument('-p', '--prefix', type=str, help='Define a username prefix', )

    def handle(self, *args, **kwargs):
        FullcsvPath = settings.MEDIA_ROOT + 'dummy_data/zomato_location.csv'
        with open(FullcsvPath, 'r') as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar="\"")
            for i, row in enumerate(reader):
                if i > 0:
                    store = Store.objects.get(id=row[0])
                    kitchen = Kitchen.objects.get(id=row[0])
                    point = Point(x=round(float(row[2]), 5), y=round(float(row[1]), 5))
                    store.location = point
                    kitchen.location = point
                    store.save()
                    kitchen.save()