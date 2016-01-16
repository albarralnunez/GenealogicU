from neomodel import (
    StructuredNode, StringProperty,
    RelationshipTo, RelationshipFrom, Relationship,
    ZeroOrOne, ArrayProperty, Booleanproperty)
from django.db import models
from django.contrib.auth.models import User
from geneTree.models import Tree


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    node_id = models.CharField()


class UserNode(StructuredNode):
    __id = StringProperty(unique_index=True)
    own = RelationshipTo(Tree, 'OWN')
