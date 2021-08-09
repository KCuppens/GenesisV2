from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Run all fixtures commands at once'

    def handle(self, *args, **kwargs):
        call_command('loaddata', 'Block', verbosity=3, database='default') 
        call_command('loaddata', 'Conf', verbosity=3, database='default') 
        call_command('loaddata', 'Icon', verbosity=3, database='default') 
        call_command('loaddata', 'DashboardConfiguration', verbosity=3, database='default') 
        call_command('loaddata', 'Module', verbosity=3, database='default') 
        call_command('loaddata', 'Page', verbosity=3, database='default') 
        call_command('loaddata', 'Translation', verbosity=3, database='default') 
        call_command('loaddata', 'User', verbosity=3, database='default') 
        call_command('loaddata', 'Group', verbosity=3, database='default') 