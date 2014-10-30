"""
Django settings for webui project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from iepy.webui.webui.settings import *

IEPY_VERSION = '0.9'
SECRET_KEY = '!qcm5^3c@^9rfvwg2=&&(eu8i%6n$hi-61c5_5c4(sjs!j1$d1'
DEBUG = True
TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/francolq/Documentos/comp/information-extraction/resoluciones-unc/resoluciones-unc/resoluciones-unc.sqlite',
    }
}
