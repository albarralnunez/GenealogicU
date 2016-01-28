from rest_framework import serializers
from .person_serializer import PersonSerializer
from django.core.exceptions import ValidationError


class DeepTreeSerializer(serializers.BaseSerializer):

    def to_representation(self, node):
        return {
            'id': node.id,
            'name': node.name,
            'description': node.description,
            'persons': PersonSerializer(node.persons.all(), many=True).data
        }


class TreeSerializer(serializers.BaseSerializer):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', False)
        super(TreeSerializer, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        name = data.get('name')
        description = data.get('description')

        if not name:
            raise ValidationError({
                'name': "name is required"
                })
        return {
            'user': self.user,
            'name': name,
            'description': description
        }

    def to_representation(self, node):
        return {
            'id': node.id,
            'name': node.name,
            'description': node.description
        }

    def create(self, validated_data):
        tree = Tree(
            name=validated_data['name'],
            user=self.user
        )
        if 'description' in validated_data:
            tree.description = validated_data['description']
        return tree.save()

    def update(self, node, validated_data):
        node.name = validated_data['name']
        if 'description' in validated_data:
            node.description = validated_data['description']
        return node.save()
