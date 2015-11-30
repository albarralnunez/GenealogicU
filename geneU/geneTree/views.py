from .models import Person
from .serializers import PersonSerializer
from neomodel import db
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import Http404
import copy

class PersonViewSet(viewsets.ModelViewSet):

    queryset = Person.nodes
    serializer_class = PersonSerializer
    lookup_field = 'id'
    permission_classes = []

    def get_object(self):
        qset = copy.deepcopy(self.queryset)
        person = list(qset.filter(
            id=self.kwargs[self.lookup_field]
            ))
        if not person:
            raise Http404("No Person matches the given query.")
        return person[0]
