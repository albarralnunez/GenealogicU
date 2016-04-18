from neomodel import (
    Relationship, StructuredNode, StringProperty)
from django.db import models
from django.contrib.auth.models import User
import geneTree.models
from django.dispatch import receiver
from django.db.models.signals import post_save
# from django.db import transaction
from django.conf import settings


class UserNode(StructuredNode):
    id = StringProperty(unique_index=True)
    own = Relationship('geneTree.models.Tree', 'OWN')


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=25, blank=True)
    private = models.BooleanField(default=False)

    '''
    @transaction.atomic
    @staticmethod
    def create_user(**kargs):
        private = False
        if 'phone_number' in kargs:
            phone_number = kargs.pop('phone_number')
        if 'private' in kargs:
            private = kargs.pop('private')
        password = kargs.pop('password')
        user = User(**kargs)
        user.set_password(password)
        user.save()
        userp = UserProfile(
            user=user,
            phone_number=phone_number,
            private=private)
        userp.save()
        UserNode(id=user.id).save()
        return user
    '''


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = UserProfile(user=instance)
        profile.save()
        node = UserNode(id=instance.id)
        node.save()
