from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Run all fixtures commands at once'

    def handle(self, *args, **kwargs):
        call_command('loaddata', 'Block Conf DashboardConfiguration Icon Module Page Translation Group User', verbosity=3, database='default')
