from .serializers import UserSerializer, UserProfileSerializer
from .permissions import UserPermissions
from .models import UserProfile
from rest_framework import viewsets
from django.http import HttpResponse
from django.template import loader
# from django.contrib.auth.models import User


def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))
    # return HttpResponseRedirect("/accounts/signup/")


class UserProfileViewSet(viewsets.ModelViewSet):

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = []
    lookup_field = 'id'

'''
class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = []
    lookup_field = 'username'
'''
