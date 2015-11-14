from .models import Person, Country
from .serializers import PersonSerializer
from neomodel import db
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

class PersonViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = Person.nodes
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        queryset = Person.nodes.filter(id=id)
        if queryset:
        	serializer = UserSerializer(user)
        else:
			raise Http404("No Person matches the given query.")
       	return Response(serializer.data)
