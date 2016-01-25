from .models import Person, Tree
from .serializers import PersonSerializer, TreeSerializer
from rest_framework import viewsets
from django.http import Http404
from rest_framework.decorators import list_route
#  from rest_framework.response import Response
import copy
from .gedcom_uploader import GedcomUploader
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from rest_framework.permissions import IsAuthenticated
from functools import partial


def handle_uploaded_file(f):

    gc = GedcomUploader(f)
    return gc.upload()

    #  for chunk in f.chunks():
    #      print str(chunk)


class TreeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    lookup_field = 'id'

    def get_serializer_class(self):
        return partial(TreeSerializer, user=self.request.user.id)

    def get_queryset(self):
        qset = Tree.nodes.filter(user=self.request.user.id)
        print list(qset)
        print list(Tree.nodes.all())[0].user
        return qset

    def get_object(self):
        qset = copy.deepcopy(self.queryset)
        try:
            return qset.get(id=self.kwargs[self.lookup_field])
        except:
            raise Http404("No Person matches the given query.")


class PersonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = Person.nodes
    serializer_class = PersonSerializer
    lookup_field = 'id'

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
