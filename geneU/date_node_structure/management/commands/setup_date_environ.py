from django.core.management.base import NoArgsCommand
from ...core import RootDate


class Command(NoArgsCommand):
    help = "setup the neo4j db for the use of the app"
    def handle_noargs(self, **options):
    	exs = list(RootDate.nodes.all())
    	if not exs:
    		RootDate().save()
    	
