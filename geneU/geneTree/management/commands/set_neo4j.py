from django.core.management.base import BaseCommand
from geneTree.tests.set_up import setup


class Command(BaseCommand):
    help = "clean all nodes and relations of the db"

    def add_arguments(self, parser):
        parser.add_argument('-s', '--set', nargs='?', help='...')

    def handle(self, *args, **options):
        se = setup()
        if not options['set']:
            se.setup()
        else:
            comm = 'se.{0}()'.format(options['set'])
            exec(comm)
