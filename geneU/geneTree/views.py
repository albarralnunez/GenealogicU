from .models import Person
from .serializers import PersonSerializer
from rest_framework import viewsets
from django.http import Http404
from rest_framework.decorators import list_route
from rest_framework.response import Response
import copy
from .gedcom_uploader import GedcomUploader


def handle_uploaded_file(f):

    gc = GedcomUploader(f)
    return gc.upload()

    #  for chunk in f.chunks():
    #      print str(chunk)


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

    @list_route(
        methods=['post'],
        url_path='gedcom')
    def upload_gedcom(self, request):
        handle_uploaded_file(request.FILES['gedcom'])
        return 'hola'
