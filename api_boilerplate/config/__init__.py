import os

DEBUG = False
ENV = 'production'  # environment hints to the flask library
ENVIRONMENT = os.environ.get('REALM')
EXTERNAL_CONFIG_DIRECTORY = os.environ.get('EXTERNAL_CONFIG_DIRECTORY')
LOG_DIRECTORY = os.environ.get('LOG_DIRECTORY')
LOG_FILE_NAME = os.environ.get('LOG_FILE_NAME')
