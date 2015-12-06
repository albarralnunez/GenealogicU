from .models import Location
from .serializers import LocationSerializer
from rest_framework import viewsets
from django.http import Http404
import copy


class LocationViewSet(viewsets.ModelViewSet):

    queryset = Location.nodes
    serializer_class = LocationSerializer
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
