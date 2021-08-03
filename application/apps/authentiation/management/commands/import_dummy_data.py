from django.core.management.base import BaseCommand, CommandError
# from django.db.models.loading import get_model
import csv
from apps.stores.models import Kitchen, Store, Item, Category
from apps.users.models import User
from config import settings


class Command(BaseCommand):
    help = "import csv file of store data and save data to the model"

    def handle(self, *args, **kwargs):
        FullcsvPath = settings.MEDIA_ROOT + 'dummy_data/zomato_full_data.csv'
        StoreModel = Store
        user = User.objects.get(id=1)
        model_fields = [f.name for f in StoreModel._meta.fields]
        with open(FullcsvPath, 'r') as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar="\"")
            fields_name = next(reader)
            for i, _ in enumerate(fields_name):
                fields_name[i] = fields_name[i].lower()
                # fields_name[i] = fields_name[i].replace(' ', '_')
                if not fields_name[i] in model_fields:
                    raise CommandError("field {} doesn't exists in {} Model".format(fields_name[i], StoreModel))
            for row in reader:
                try:
                    store_obj = StoreModel()
                    for i, field in enumerate(row):
                        setattr(store_obj, fields_name[i], field.strip())
                    store_obj.created_by = user
                    store_obj.save()
                except Exception as e:
                    raise CommandError(e)

            """ add kitchen to the store"""
            KitchencsvPath = settings.MEDIA_ROOT + 'dummy_data/zomato_kitchen.csv'
            KitchenModel = Kitchen
            # user = User.objects.get(id=1)
            model_fields = [f.name for f in KitchenModel._meta.fields]

            with open(KitchencsvPath, 'r') as csvFile:
                reader = csv.reader(csvFile, delimiter=',', quotechar="\"")
                fields_name = next(reader)
                for i, _ in enumerate(fields_name):
                    fields_name[i] = fields_name[i].lower()
                    # fields_name[i] = fields_name[i].replace(' ', '_')
                    if not fields_name[i] in model_fields:
                        raise CommandError("field {} doesn't exists in {} Model".format(fields_name[i], KitchenModel))
                kitchen_id = 50
                for row in reader:
                    try:
                        kitchen_obj = KitchenModel()
                        for i, field in enumerate(row):
                            setattr(kitchen_obj, fields_name[i], field.strip())
                        store = Store.objects.get(id=kitchen_id)
                        kitchen_obj.store=store
                        kitchen_obj.created_by = user
                        kitchen_obj.save()
                        kitchen_id = kitchen_id + 1
                    except Exception as e:
                        raise CommandError(e)
        """ add category the category model"""

        CategorycsvPath = settings.MEDIA_ROOT + 'dummy_data/zomato_category.csv'
        CategoryModel = Category
        # user = User.objects.get(id=1)
        model_fields = [f.name for f in CategoryModel._meta.fields]
        with open(CategorycsvPath, 'r') as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar="\"")
            fields_name = next(reader)
            for i, _ in enumerate(fields_name):
                fields_name[i] = fields_name[i].lower()
                # fields_name[i] = fields_name[i].replace(' ', '_')
                if not fields_name[i] in model_fields:
                    raise CommandError("field {} doesn't exists in {} Model".format(fields_name[i], CategoryModel))
            category_id = 50
            for row in reader:
                try:
                    category_obj = CategoryModel()
                    for i, field in enumerate(row):
                        setattr(category_obj, fields_name[i], field.strip())
                    kitchen = Kitchen.objects.get(id=category_id)
                    category_obj.kitchen=kitchen
                    category_obj.store=kitchen.store
                    category_obj.created_by = user
                    category_obj.save()
                    category_id = category_id + 1
                except Exception as e:
                    raise CommandError(e)
        """add items to the item model"""

        ItemcsvPath = settings.MEDIA_ROOT + 'dummy_data/zomato_item.csv'
        ItemModel = Item
        # user = User.objects.get(id=1)
        model_fields = [f.name for f in ItemModel._meta.fields]
        with open(ItemcsvPath, 'r') as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar="\"")
            fields_name = next(reader)
            for i, _ in enumerate(fields_name):
                fields_name[i] = fields_name[i].lower()
                # fields_name[i] = fields_name[i].replace(' ', '_')
                if not fields_name[i] in model_fields:
                    print(fields_name)
                    raise CommandError("field {} doesn't exists in {} Model".format(fields_name[i], ItemModel))
            item_id = 50
            for row in reader:
                try:
                    item_obj = ItemModel()
                    for i, field in enumerate(row):
                        setattr(item_obj, fields_name[i], field.strip())
                    kitchen = Kitchen.objects.get(id=item_id)
                    category = Category.objects.get(id=item_id)
                    item_obj.category = category
                    item_obj.kitchen = kitchen
                    item_obj.store = kitchen.store
                    item_obj.delivery_charges = 45.00
                    item_obj.created_by = user
                    # item_obj.mobile = 8888888888
                    item_obj.save()
                    item_id = item_id + 1
                    if item_id == 364:
                        item_id = 50
                except Exception as e:
                    raise CommandError(e)
