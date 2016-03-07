from geneU.celery import app
from geneU.settings import HOSTNAME
from django.core.mail import send_mail


@app.task(name='geenTree.geneU.gedcom_uploader_task')
def gedcom_uploader_task(fil, tree):
    rec = ['albarralnunez@gmail.com']
    sen = 'geneU@localhost.com'

    try:
        fil.upload(tree)
        message = (
            "Tree {name} was succesfully created.\n"
            "Check it at {host}/tree/{id}/.").format(
                name=tree.name, id=tree.id, host=HOSTNAME)
        # user = list(ser.user.all())[0].id
        # mail = UserProfile.objects.get(id=user).user.email
        send_mail(
            'Tree succesfully created',
            message,
            sen,
            rec
        )
        return True
    except:
        message = 'Upload of tree {tree} failed.'.format(tree=tree.name)
        # user = list(ser.user.all())[0].id
        # mail = UserProfile.objects.get(id=user).user.email
        send_mail(
            'Tree succesfully created',
            message,
            sen,
            rec
        )
        return False


@app.task(name='geneU.geenTree.check_coincidence')
def check_coincidence_task(per):
    from .models import Person

    main = Person.nodes.get(id=per)

    rec = ['albarralnunez@gmail.com']
    sen = 'geneU@localhost.com'

    send_mail(
        'check executed',
        ':)',
        sen,
        rec
    )
