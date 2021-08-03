import os
from config.settings import BASE_DIR

DEBUG = True

ALLOWED_HOSTS = ['*']

BASE_URL = 'http://192.168.1.40:8000/'
# BASE_URL_NO_TRAILING = 'http://localhost:8002'
#
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

# GEOS_LIBRARY_PATH = r'C:\OSGeo4W64\bin\geos_c.dll'
# GDAL_LIBRARY_PATH = r'C:\OSGeo4W64\bin\gdal111.dll'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'pkbpy2',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '',
    },
}

# BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
