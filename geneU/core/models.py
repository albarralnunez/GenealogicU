from neomodel import (
    StructuredNode, StringProperty,
    RelationshipTo)
from django.db import models
from django.contrib.auth.models import User
from geneTree.models import Tree


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    node_id = models.CharField(max_length=25)


class UserNode(StructuredNode):
    __id = StringProperty(unique_index=True)
    own = RelationshipTo(Tree, 'OWN')
