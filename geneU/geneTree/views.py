from .models import Person, Country
from .serializers import PersonSerializer
from neomodel import db
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import Http404

class PersonViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = Person.nodes
        serializer = PersonSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Person.nodes.filter(id=pk)[0]
        if queryset:
        	serializer = PersonSerializer(queryset[0])
        else:
			raise Http404("No Person matches the given query.")
       	return Response(serializer.data)
