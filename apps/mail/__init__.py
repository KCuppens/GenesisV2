
from ast import literal_eval
from os.path import dirname, join

with open(join(dirname(__file__), 'version.txt'), 'r') as fh:
    VERSION = literal_eval(fh.read())

default_app_config = 'apps.mail.apps.MailConfig'