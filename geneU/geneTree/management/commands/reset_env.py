from django.core.management.base import NoArgsCommand
import subprocess


class Command(NoArgsCommand):
    help = "clean all nodes and relations of the db"

    def handle_noargs(self, **options):

        subprocess.call(["python", "manage.py", "clean_neo_db"])
        subprocess.call(["python", "manage.py", "setup_loc_environ"])
        subprocess.call(["python", "manage.py", "setup_date_environ"])

        subprocess.call(["python", "manage.py", "reset_db"])
        subprocess.call(["python", "manage.py", "migrate"])
        subprocess.call([
                            "python", "manage.py", "createsuperuser",
                            "--username=admin", "--email=admin@geneu.com"
                        ])
        subprocess.call(["python", "manage.py", "set_neo4j"])
