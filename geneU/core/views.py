from .serializers import UserProfileSerializer
from .models import UserProfile
from rest_framework import viewsets
from django.http import HttpResponse
from django.template import loader
# from django.contrib.auth.models import User
import account.views
from .forms import SignupForm


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


"""
class SignupView(account.views.SignupView):
    form_class = SignupForm

    def after_signup(self, form):
        self.create_profile(form)
        super(SignupView, self).after_signup(form)

    def create_profile(self, form):
        UserProfile.objects.create(
            user=self.created_user,
            #name = form.cleaned_data['name']
        )


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = []
    lookup_field = 'username'
"""
