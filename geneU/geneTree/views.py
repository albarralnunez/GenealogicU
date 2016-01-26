from .models import Person, Tree
from .serializers import TreeSerializer, DeepTreeSerializer
from .person_serializer import PersonSerializer
from rest_framework import viewsets
from django.http import Http404
from rest_framework.decorators import detail_route
from rest_framework.response import Response
import copy
from .gedcom_uploader import GedcomUploader
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from rest_framework.permissions import IsAuthenticated
from functools import partial


def handle_uploaded_file(f, tree):
    gc = GedcomUploader(f, tree)
    return gc.upload()

    #  for chunk in f.chunks():
    #      print str(chunk)


class TreeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    lookup_field = 'id'

    def get_serializer_class(self):
        return partial(TreeSerializer, user=self.request.user.id)

    def get_queryset(self):
        return Tree.nodes.filter(user=self.request.user.id)

    def get_object(self):
        qset = copy.deepcopy(self.get_queryset())
        try:
            return qset.get(id=self.kwargs[self.lookup_field])
        except:
            raise Http404("No Person matches the given query.")

    @detail_route(
        methods=['post'],
        url_path='gedcom')
    def upload_gedcom(self, request, id=None):
        handle_uploaded_file(
            request.FILES['gedcom'],
            self.get_object()
        )
        return Response(DeepTreeSerializer(self.get_object()).data)


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
