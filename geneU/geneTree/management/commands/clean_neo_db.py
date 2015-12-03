from django.core.management.base import NoArgsCommand
from neomodel import db
import subprocess


class Command(NoArgsCommand):
    help = "clean all nodes and relations of the db"

    def handle_noargs(self, **options):
        db.cypher_query(
            '''
            MATCH (n)\
            OPTIONAL MATCH (n)-[r]-()\
            WITH n,r LIMIT 100000 DELETE n,r;\
            '''
        )
        subprocess.call(["python", "manage.py", "setup_loc_environ"])
        subprocess.call(["python", "manage.py", "setup_date_environ"])
