from .serializers_person import PersonSerializer
import geneTree.models_person as models_person
from .gedcom_uploader import GedcomUploader
from core.models import UserProfile, UserNode
from rest_framework import serializers
from django.core.exceptions import ValidationError
from .tasks import gedcom_uploader_task


class DeepTreeSerializer(serializers.BaseSerializer):

    def to_representation(self, node):
        from core.serializers import UserProfileSerializer
        usern = list(node.user.all())[0]
        if usern:
            userp = UserProfile.objects.get(id=usern.id)

        return {
            'url': '/tree/{id}'.format(id=node.id),
            'user': UserProfileSerializer(userp, simple=True).data,
            'name': node.name,
            'description': node.description,
            'persons': PersonSerializer(
                node.get_persons(), many=True).data
        }


class TreeSerializer(serializers.BaseSerializer):

    def __init__(self, *args, **kwargs):
        self.simple = kwargs.pop('simple', False)
        self.user = kwargs.pop('user', None)
        super(TreeSerializer, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        name = data.get('name')
        description = data.get('description')
        private = data.get('private')
        if not name:
            raise ValidationError({
                'name': "name is required"
                })

        private = private if private else 'False'
        private = private == 'True'

        return {
            'name': name,
            'description': description,
            'private': private
        }

    def to_representation(self, node):
        from core.serializers import UserProfileSerializer
        usern = list(node.user.all())[0]
        if usern:
            userp = UserProfile.objects.get(id=usern.id)
        return {
            'url': '/tree/{id}'.format(id=node.id),
            'user': UserProfileSerializer(userp, simple=True).data,
            'name': node.name,
            'description': node.description
        }

    def create(self, validated_data):
        user = UserNode.nodes.get(id=self.user)
        tree = models_person.Tree(
            name=validated_data['name'],
            private=validated_data['private']
        )
        if 'description' in validated_data:
            tree.description = validated_data['description']
        tree.save()
        tree.user.connect(user)
        return tree

    def update(self, node, validated_data):
        node.name = validated_data['name']
        node.private = validated_data['private']
        if 'description' in validated_data:
            node.description = validated_data['description']
        return node.save()


class GedcomSerializer(TreeSerializer):

    def to_internal_value(self, data):

        try:
            fil = data.pop('file')
        except:
            raise ValidationError({
                'file': "file is required"
                })
        res = super(GedcomSerializer, self).to_internal_value(data)
        res['file'] = GedcomUploader(fil[0])
        # except:
        #     raise ValueError('detail: file has invalid format')

        return res

    def to_representation(self, node):
        return {
            'tree': TreeSerializer(node).data
        }

    def create(self, validated_data):
        fil = validated_data.pop('file')
        res = super(GedcomSerializer, self).create(validated_data)
        gedcom_uploader_task.apply_async((fil, res))
        return res
