import string, random, os, time, json
from django.conf import settings
from PIL import Image
# from django.core.mail.message import EmailMessage
# from django.core.mail import get_connection
# from django.contrib.auth import get_user_model
# from shared.users.models import LoginLog
from django.utils import timezone
# from django.contrib.gis.geoip2 import GeoIP2
# import httpagentparser
import shutil
import requests
import random
import jwt
from datetime import date, datetime
from pytz import timezone as tz


def file_upload_handler(file_object, dir, filename=None, resize=False, dimension=(), extension='JPEG'):
    """
    Upload the passed file as file_object, in dir
    if filename is None( which is default), it will generate by own
    otherwise will use the passed filename from param

    If resize true, dimension will be required
    :param file_object: File
    :param dir:    string
    :param filename: string
    :param resize: boolean
    :param resize: tuple
    :param extension: string ( JPEG, PNG )
    :return: string file_name if success else False
    """
    return_value = False
    if file_object:
        file_name = filename if filename is not None else str(random.randint(1000, 10000)) + '_' + str(
            int(time.time())) + '_' + file_object.name
        try:
            if resize:
                if len(dimension) == 2:
                    im = Image.open(file_object)
                    im.thumbnail(dimension, Image.ANTIALIAS)
                    im.save(dir + file_name, extension)
                    return_value = file_name
                else:
                    raise ValueError('Dimension is required, when resize is True.')
            else:
                with open(dir + file_name, 'wb+') as destination:
                    for chunk in file_object.chunks():
                        destination.write(chunk)
                return_value = file_name
        except Exception as e:
            print('hiii',e)
            raise e
    return return_value


def image_upload_handler(image_object, root_dir, filename=None, resize=False, dimension=(), extension='JPEG',
                         quality=100):
    return_value = False
    if image_object:
        file_name = filename if filename is not None else str(random.randint(10000, 10000000)) + '_' + str(
            int(time.time())) + '_' + image_object.name
        try:
            im = Image.open(image_object)
            if resize:
                if len(dimension) == 2:
                    im.thumbnail(dimension, Image.ANTIALIAS)
                else:
                    raise ValueError('Dimension is required, when resize is True.')

            im.save(root_dir + file_name, extension, quality=quality)
            image_to_thumb = im
            image_to_thumb.thumbnail((250, 250), Image.ANTIALIAS)
            image_to_thumb.save(root_dir + "T_" + file_name, extension, quality=quality)
            return_value = file_name
        except Exception as e:
            raise e
    return return_value


def image_thumb_upload_handler(image_dir, root_dir, filename=None, resize=False, dimension=(), extension='JPEG',
                               quality=100):
    return_value = False
    if image_dir:
        file_name = filename if filename is not None else str(random.randint(10000, 10000000)) + '_' + str(
            int(time.time()))
        try:
            im = image_dir
            if resize:
                if len(dimension) == 2:
                    im.thumbnail(dimension, Image.ANTIALIAS)
                else:
                    raise ValueError('Dimension is required, when resize is True.')

            image_to_thumb = im
            image_to_thumb.thumbnail((250, 250), Image.ANTIALIAS)
            image_to_thumb.save(root_dir + "T_" + file_name, extension, quality=quality)

            return_value = file_name
        except Exception as e:
            print(e)
            raise e
    return return_value


def join_string(string):
    name = string.split(' ')
    concate_name = ''.join(name)
    return concate_name


def copy_file(src, dst):
    try:
        shutil.copy(src, dst)
        return_value = True
    except OSError as oe:
        print('adsfsdf')
        print(oe)
        raise oe
    except Exception as e:
        raise e
    return return_value


def copy_dir(src, dst):
    try:
        shutil.copytree(src, dst)
        return_value = True
    except OSError as oe:
        raise oe
    except Exception as e:
        raise e
    return return_value


def make_dir(dirname):
    """
    Creates new directory if not exists
    :param dirname: String
    :return: String
    """
    try:
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        return dirname
    except Exception as e:

        raise e


def remove_file(dir, filename):
    """
    Remove a file from specified directory
    :param dir:
    :param filename:
    :return: boolean
    """
    return_value = False
    try:
        if dir and filename:
            full_path = dir + filename
            if os.path.exists(full_path):
                os.remove(full_path)
            return_value = True
    except Exception as e:
        raise e
    return return_value


def remove_dir(dir_tree, ignore_errors=False):
    """
    Remove a directory completely, either empty or not
    :param dir_tree: ex : /full/path/of/directory/
    :param ignore_errors : By default rmtree(below) fails on folder trees containing read-only files.
    :return: boolean
    """
    try:
        if os.path.exists(dir_tree):
            shutil.rmtree(dir_tree, ignore_errors=ignore_errors)
        return_value = True
    except Exception as e:
        raise e
    return return_value


def get_client_ip(request):
    """
    Will return requested client ip address
    :param request: HttpRequest
    :return: string
    """
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    except Exception:
        ip = ''
    return ip


def base_token_factory(length=100, prepend=''):
    """
    Returns random string
    Length defined by length param, default is 100
    Prepend, If wants to add some string before this

    If prepend string length is longer than length, then it will follow default
    not add the prepend


    :param length:
    :param prepend:
    :return: generated_string
    """
    final_length = length
    generated_string = ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
        range(final_length))
    if prepend and type(prepend) == str and len(prepend) < length:
        final_length -= len(prepend)
        generated_string = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
            range(final_length))
        generated_string = prepend + generated_string
    return generated_string


def get_auth_token():
    """
    Returns 100 character long random string
    :return: String generated_string
    """
    generated_string = base_token_factory(length=60)
    return generated_string


def get_global_login_token():
    """
    Returns 100 character long random string
    :return: String generated_string
    """
    generated_string = base_token_factory(length=60)
    return generated_string


def get_password_rest_token():
    """
    Returns 50 character long random string
    :return: String generated_string
    """
    generated_string = base_token_factory(length=50)
    return generated_string


def generate_otp(digit):
    """
    Generate n digit random number for otp. digit=n
    :param digit:
    :return: Integer
    """
    lower = 10 ** (digit - 1)
    upper = 10 ** digit - 1
    return random.randint(lower, upper)


def generate_password():
    """
    Generate 8 char alphanumenric password for newly create user by admin/owner/manager.html for apps
    :param None:
    :return: string
    """
    return ''.join(random.choice('0123456789ABCDEF') for i in range(8))


def capture_login_info(request, user, mode_api=False):
    pass
    # if mode_api:
    #     new_session_key = get_auth_token()  # Enable to request this function in browser and api views
    # else:
    #     new_session_key = request.session.session_key
    #
    # ip_address = get_client_ip(request)
    # country_name = get_country_name(ip_address)
    # platform = detect_os_browser(request)
    #
    # created_obj = LoginLog.objects.create(
    #     login_ip = ip_address,
    #     login_country = country_name,
    #     login_os = platform.get('os'),
    #     login_browser = platform.get('browser'),
    #     login_platform = platform.get('platform'),
    #     login_time = timezone.now(),
    #     logout_time = None,
    #     status = 1,
    #     user=user
    # )
    # return {
    #     'session_key': new_session_key,
    #     'ip_address' : ip_address,
    #     'country_name' : country_name,
    #     'platform' : platform,
    #     'log_object' : created_obj
    # }


def get_country_by_ip(request):
    country_name = None
    client_ip = get_client_ip(request)
    if client_ip:
        country_name = get_country_name(client_ip)
    return country_name


def get_country_name(ip_address):
    pass
    # country_name = ''
    # if ip_address:
    #     try:
    #         country = GeoIP2().country(ip_address)
    #         country_name = country.get('country_name')
    #     except:
    #         country_name = ''
    # return country_name


def detect_os_browser(request):
    pass
    # data = {'platform' : '', 'os' : '', 'browser' : ''}
    # try:
    #     agent = request.META['HTTP_USER_AGENT']
    #     detected_data = httpagentparser.detect(agent)
    #     platform = detected_data.get('platform', None)
    #     if platform and 'name' in platform:
    #         data['platform'] = platform.get('name')
    #         if  'version' in platform and platform.get('version'):
    #             data['platform'] = data['platform'] + ' ' +  platform.get('version')
    #     if 'os' in detected_data:
    #         tmp_os = detected_data.get('os')
    #         if 'name' in tmp_os and tmp_os.get('name'):
    #             data['os'] = tmp_os.get('name')
    #     if 'browser' in detected_data:
    #         tmp_browser = detected_data.get('browser')
    #         if 'name' in tmp_browser and tmp_browser.get('name'):
    #             data['browser'] = tmp_browser.get('name')
    #         if 'version' in tmp_browser and tmp_browser.get('version'):
    #             data['browser'] = data['browser'] + ' ' + tmp_browser.get('version')
    # except:
    #     pass
    # return data


def get_unique_id(length=5):
    """
    Generates unique id for any entity
    With current timestamp with random 5 characters
    :param : length (optional)
    :return: string
    """
    return str(int(time.time())) + base_token_factory(length)


def send_push_notification(payload={}, user=None):
    """
       Returns response from server
       Send push notification to user by user id

       If prepend string length is longer than length, then it will follow default
       not add the prepend

       :param payload:
       :param User object :
       :return: dict response with status : true/false
    """

    if user:
        raise Exception("User expected in param 2.")

    url = settings.SOCKET_URL + "api/v1/push"
    headers = {
        'Authorization': user.global_login_token,
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
    }
    payload = json.dumps(payload)
    response = requests.request("POST", url, data=payload, headers=headers)
    return json.loads(response.text)


def convert_to_object(object, of_class=None, from_field=""):
    if object and not isinstance(object, of_class):
        try:
            object = of_class.objects.get(**{from_field: object})
        except Exception:
            object = None
    return object


def get_token_details(token):
    secret = 'qwertyuiopasdfghjklzxcvbnm123456'
    decoded = jwt.decode(token, secret, verify=False)
    return decoded


def time_check(obj):
    indian_time = tz('Asia/Kolkata')
    time = datetime.now(indian_time).time()
    if (type(obj.opening_time)) != 'str':
        if obj.opening_time <= time and obj.closing_time >= time:
            return True
        else:
            return False
    else:
        return obj.status


def discount_active(discount):
    indian_time = tz('Asia/Kolkata')
    if discount.discount.from_date is not None and discount.discount.to_date is not None:
        now = date.today()
        time = datetime.now(indian_time).time()
        if discount.discount.from_date.month <= now.month and discount.discount.to_date.month > now.month:
            return True
        elif discount.discount.from_date.month == now.month and discount.discount.to_date.month == now.month:
            if discount.discount.from_date.day <= now.day and discount.discount.to_date.day > now.day:
                return True
            elif discount.discount.from_date.day <= now.day and discount.discount.to_date.day == now.day:
                if discount.discount.to_time >= time and discount.discount.from_time <= time:
                    return True
    return False