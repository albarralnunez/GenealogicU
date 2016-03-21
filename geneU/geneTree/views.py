import geneTree.models_person as models_person
import geneTree.serializers_tree as serializer_tree
import geneTree.serializers_person as serializer_person
from rest_framework import viewsets, status
from core.models import UserProfile
from django.http import Http404
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from rest_framework.permissions import IsAuthenticated
from functools import partial
from geneTree.tasks import check_coincidence_task
import copy


class TreeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    lookup_field = 'id'
    queryset = models_person.Tree.nodes

    def get_serializer_class(self):
        return partial(
            serializer_tree.TreeSerializer,
            user=self.request.user.userprofile.id)

    def get_object(self):
        qset = copy.deepcopy(self.get_queryset())
        try:
            return qset.get(id=self.kwargs[self.lookup_field])
        except:
            raise Http404("No Tree matches the given query.")

    @list_route(
        methods=['post'],
        url_path='gedcom')
    def upload_gedcom_tree(self, request):
        serializer = serializer_tree.GedcomSerializer(
            data=request.data, user=request.user.id)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data,
                        status=status.HTTP_202_ACCEPTED)

    @detail_route(
        methods=['get'],
        url_path='members')
    def get_members(self, request, id=None):
        obj = self.get_object()
        tree_userp = UserProfile.objects.get(id=obj.user.all()[0].id)
        if obj.private and not request.user.userprofile == tree_userp:
            return Response('{detail: private tree}',
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                serializer_tree.DeepTreeSerializer(self.get_object()).data
            )

    @detail_route(
        methods=['post'],
        url_path='person')
    def post_person(self, request, id=None):
        request.data['tree'] = id
        person_serializer = \
            serializer_person.PersonSerializer(data=request.data)
        if person_serializer.is_valid():
            person_serializer.save()
            return Response(person_serializer.data)
        else:
            return Response(person_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class PersonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = models_person.Person.nodes
    serializer_class = serializer_person.PersonSerializer
    lookup_field = 'id'

    def pickle_person(per):
        print("pickling a C instance...")
        return models_person.Person.nodes

    def get_object(self):
        qset = copy.deepcopy(self.queryset)
        try:
            res = qset.get(id=self.kwargs[self.lookup_field])
            # res = pickle.load(res)
            return res
        except:
            raise Http404("No Person matches the given query.")

    @detail_route(
        methods=['post'],
        url_path='marriage')
    def post_marriage(self, request, id=None):
        request.data['spouse2'] = id
        marriage_serializer = \
            serializer_person.MarriageSerializer(data=request.data)
        if marriage_serializer.is_valid():
            marriage_serializer.save()
            return Response(marriage_serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(marriage_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @detail_route(
        methods=['post'],
        url_path='divorce')
    def post_divorce(self, request, id=None):
        request.data['spouse2'] = id
        divorce_serializer = \
            serializer_person.DivorceSerializer(data=request.data)
        if divorce_serializer.is_valid():
            divorce_serializer.save()
            return Response(divorce_serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(divorce_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @detail_route(
        methods=['post'],
        url_path='birth')
    def post_birth(self, request, id=None):
        request.data['son'] = id
        birth_serializer = \
            serializer_person.BirthSerializer(data=request.data)
        if birth_serializer.is_valid():
            birth_serializer.save()
            return Response(birth_serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(birth_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @detail_route(
        methods=['post'],
        url_path='death')
    def post_death(self, request, id=None):
        request.data['death'] = id
        serializer = \
            serializer_person.DeathSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @detail_route(
        methods=['post'],
        url_path='adoption')
    def post_adoption(self, request, id=None):
        request.data['son'] = id
        serializer = \
            serializer_person.AdoptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @detail_route(
        methods=['post'],
        url_path='lived')
    def post_lived(self, request, id=None):
        request.data['person'] = id
        serializer = \
            serializer_person.LivedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @detail_route(
        methods=['get'],
        url_path='search')
    def search_similars(self, request, id=None):
        check_coincidence_task.apply_async((id,))
        return Response('{detail: Accepted}',
                        status=status.HTTP_202_ACCEPTED)


class MarriageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = models_person.Marriage.nodes
    serializer_class = serializer_person.MarriageSerializer
    lookup_field = 'id'

    def get_object(self):
        qset = copy.deepcopy(self.queryset)
        try:
            return qset.get(id=self.kwargs[self.lookup_field])
        except:
            raise Http404("No Marriage matches the given query.")


class DivorceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = models_person.Divorce.nodes
    serializer_class = serializer_person.DivorceSerializer
    lookup_field = 'id'

    def get_object(self):
        qset = copy.deepcopy(self.queryset)
        try:
            return qset.get(id=self.kwargs[self.lookup_field])
        except:
            raise Http404("No Divorce matches the given query.")


class BirthViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = models_person.Birth.nodes
    serializer_class = serializer_person.BirthSerializer
    lookup_field = 'id'

    def get_object(self):
        qset = copy.deepcopy(self.queryset)
        try:
            return qset.get(id=self.kwargs[self.lookup_field])
        except:
            raise Http404("No Birth matches the given query.")


class DeathViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = models_person.Death.nodes
    serializer_class = serializer_person.DeathSerializer
    lookup_field = 'id'

    def get_object(self):
        qset = copy.deepcopy(self.queryset)
        try:
            return qset.get(id=self.kwargs[self.lookup_field])
        except:
            raise Http404("No Death matches the given query.")


class AdoptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = models_person.Adoption.nodes
    serializer_class = serializer_person.AdoptionSerializer
    lookup_field = 'id'

    def get_object(self):
        qset = copy.deepcopy(self.queryset)
        try:
            return qset.get(id=self.kwargs[self.lookup_field])
        except:
            raise Http404("No Adoption matches the given query.")


class LivedViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = models_person.Lived.nodes
    serializer_class = serializer_person.LivedSerializer
    lookup_field = 'id'

    def get_object(self):
        qset = copy.deepcopy(self.queryset)
        try:
            return qset.get(id=self.kwargs[self.lookup_field])
        except:
            raise Http404("No Lived matches the given query.")
