from django.core.management.base import BaseCommand, CommandError
# from django.db.models.loading import get_model
import csv
from apps.stores.models import Kitchen, Store, Item, Category
from libraries.Functions import join_string, image_thumb_upload_handler
from config import settings
from PIL import Image


class Command(BaseCommand):
    help = "compress image"

    def handle(self, *args, **kwargs):
        stores = Store.objects.all()
        for obj in stores:
            store_name = join_string(obj.name)
            if obj.image:
                root_directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                                 settings.CUSTOM_DIRS['IMAGE_DIR']

                directory_image = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                                  settings.CUSTOM_DIRS['IMAGE_DIR'] + obj.image

                img  = Image.open(directory_image)
                img_path = image_thumb_upload_handler(img, root_directory)
                obj.image_thumb = ("{}".format("T_" + img_path)) if img_path else ""
                obj.save()
            if obj.logo:
                directory_logo = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                                 settings.CUSTOM_DIRS['LOGO_DIR'] + obj.logo
                logo_directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                                 settings.CUSTOM_DIRS['LOGO_DIR']

                logo = Image.open(directory_logo)


                logo_path = image_thumb_upload_handler(logo, logo_directory)

                obj.logo_thumb = ("{}".format("T_" + logo_path)) if logo_path else ""
                obj.save()
        kitchen = Kitchen.objects.all()
        for obj in kitchen:
            store_name, kitchen_name = join_string(obj.store.name), join_string(obj.name)
            if obj.image:

                image_directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                              settings.CUSTOM_DIRS[
                                  'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR']

                directory_image = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                              settings.CUSTOM_DIRS[
                                  'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS['IMAGE_DIR'] + obj.image
                img = Image.open(directory_image)
                img_path = image_thumb_upload_handler(img, image_directory)

                obj.image_thumb = ("{}".format("T_" + img_path)) if img_path else ""
                obj.save()

            if obj.logo:

                directory_logo = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                         settings.CUSTOM_DIRS[
                             'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS['LOGO_DIR'] + obj.logo
                logo_directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                                 settings.CUSTOM_DIRS[
                                     'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS['LOGO_DIR']

                logo = Image.open(directory_logo)

                logo_path = image_thumb_upload_handler(logo, logo_directory)
                obj.logo_thumb = ("{}".format("T_" + logo_path)) if logo_path else ""
                obj.save()
        # category = Category.objects.all()
        # for obj in category:
        #     if obj.image:
        #         store_name, kitchen_name, category_name = join_string(obj.kitchen.store.name), \
        #                                                   join_string(obj.kitchen.name), join_string(
        #             obj.name)
        #
        #         image_directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
        #                           settings.CUSTOM_DIRS[
        #                               'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS[
        #                               'CATEGORY_DIR'] + category_name + '/' + settings.CUSTOM_DIRS[
        #                               'IMAGE_DIR'] + obj.image
        #         root_directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
        #                          settings.CUSTOM_DIRS[
        #                              'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS[
        #                              'CATEGORY_DIR'] + category_name + '/' + settings.CUSTOM_DIRS[
        #                              'IMAGE_DIR']
        #         img = Image.open(image_directory)
        #         img_path = image_thumb_upload_handler(img, root_directory)
        #
        #         obj.image = ("{}".format("T_" + img_path+".jpeg")) if img_path else ""
        #         obj.save()

        items = Item.objects.all()
        for obj in items:
            if obj.image:
                store_name, kitchen_name, category_name, item_name = join_string(obj.category.kitchen.store.name), \
                                                                     join_string(obj.category.kitchen.name), join_string(
                    obj.category.name), join_string(obj.name)

                image_directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                                  settings.CUSTOM_DIRS[
                                      'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS[
                                      'CATEGORY_DIR'] + category_name + '/' + \
                                  settings.CUSTOM_DIRS['ITEM_DIR'] + item_name + '/' + settings.CUSTOM_DIRS[
                                      'IMAGE_DIR'] + obj.image
                root_directory = settings.MEDIA_ROOT + settings.CUSTOM_DIRS['STORE_DIR'] + store_name + '/' + \
                                 settings.CUSTOM_DIRS[
                                     'KITCHEN_DIR'] + kitchen_name + '/' + settings.CUSTOM_DIRS[
                                     'CATEGORY_DIR'] + category_name + '/' + \
                                 settings.CUSTOM_DIRS['ITEM_DIR'] + item_name + '/' + settings.CUSTOM_DIRS[
                                     'IMAGE_DIR']
                img = Image.open(image_directory)
                img_path = image_thumb_upload_handler(img, root_directory)

                obj.image_thumb = ("{}".format("T_" + img_path)) if img_path else ""
                obj.save()
