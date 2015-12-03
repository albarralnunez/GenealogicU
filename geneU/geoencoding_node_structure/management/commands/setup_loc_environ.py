from django.core.management.base import NoArgsCommand
from ...core import RootLocation


class Command(NoArgsCommand):
    help = "setup the neo4j db for the use of the app"

    def handle_noargs(self, **options):
        exs = list(RootLocation.nodes.all())
        if not exs:
            RootLocation().save()
