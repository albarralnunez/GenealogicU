from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    help = "clean all nodes and relations of the db"

    def add_arguments(self, parser):
        parser.add_argument('-s', '--set', nargs='?', help='...')

    def handle(self, *args, **options):

        subprocess.call(["python", "manage.py", "clean_neo_db"])
        subprocess.call(["python", "manage.py", "setup_loc_environ"])
        subprocess.call(["python", "manage.py", "setup_date_environ"])

        subprocess.call(["python", "manage.py", "reset_db"])
        subprocess.call(["python", "manage.py", "migrate"])
        subprocess.call([
                            "python", "manage.py", "createsuperuser",
                            "--username=admin", "--email=admin@geneu.com"
                        ])
        set_nj4 = ["python", "manage.py", "set_neo4j"]
        if options['set']:
            set_nj4 += ["-s", options['set']]
        subprocess.call(set_nj4)
