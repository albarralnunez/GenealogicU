from django.core.management.base import NoArgsCommand
from geneTree.tests.set_up import setup


class Command(NoArgsCommand):
    help = "clean all nodes and relations of the db"

    def handle_noargs(self, **options):
        set_up = setup()
        set_up.setup()
