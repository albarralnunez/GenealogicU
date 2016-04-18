import core.views as views_core
import geneTree.views as views_genetree
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers, urls
# from oauth2_provider import login

admin.autodiscover()

router = routers.DefaultRouter()
router.register(
    r'user',
    views_core.UserProfileViewSet,
    base_name='user')
router.register(
    r'person',
    views_genetree.PersonViewSet,
    base_name='person')
router.register(
    r'tree',
    views_genetree.TreeViewSet,
    base_name='tree')
router.register(
    r'marriage',
    views_genetree.MarriageViewSet,
    base_name='marriage')
router.register(
    r'divorce',
    views_genetree.DivorceViewSet,
    base_name='divorce')
router.register(
    r'birth',
    views_genetree.BirthViewSet,
    base_name='birth')
router.register(
    r'death',
    views_genetree.DeathViewSet,
    base_name='death')
router.register(
    r'adoption',
    views_genetree.AdoptionViewSet,
    base_name='adoption')
router.register(
    r'lived',
    views_genetree.LivedViewSet,
    base_name='lived')
# router.register(
#     r'user',
#     UserViewSet,
#     base_name='user')

urlpatterns = [
    url(r'^$', views_core.index, name='home'),
    # url(r'^account/signup/$',
    #     views_core.SignupView.as_view(),
    #     name='account_signup'),
    url(r"^accounts/", include("account.urls")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^api-auth/',
        include(urls, namespace='rest_framework'))
]

urlpatterns += router.urls
