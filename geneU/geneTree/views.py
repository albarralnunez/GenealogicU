from .models import Person
from .serializers import PersonSerializer
from rest_framework import viewsets
from django.http import Http404
import copy


class PersonViewSet(viewsets.ModelViewSet):

    queryset = Person.nodes
    serializer_class = PersonSerializer
    lookup_field = 'id'
    permission_classes = []

    def get_object(self):
        qset = copy.deepcopy(self.queryset)
        try:
            return qset.get(id=self.kwargs[self.lookup_field])
        except:
            raise Http404("No Person matches the given query.")
