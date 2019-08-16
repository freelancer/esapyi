import os

DEBUG = False
ENV = 'production'  # environment hints to the flask library
ENVIRONMENT = os.environ.get('REALM')
EXTERNAL_CONFIG_DIRECTORY = os.environ.get('EXTERNAL_CONFIG_DIRECTORY')
