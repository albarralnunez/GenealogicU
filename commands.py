#send mail throw shell plus
from django.core.mail import send_mail
send_mail('a', 'b', 'u@u.com', ['a@a.com'])

#start neo4j ./bin/neo4j start

#start worker celery
celery -A geneU worker -l info

# test
./manage.py test geneTree.tests.tests_models

