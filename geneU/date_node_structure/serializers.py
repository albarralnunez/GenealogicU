from .core import NodeDate
from rest_framework import serializers


class DateSerializer(serializers.BaseSerializer):

    def to_internal_value(self, data):

        date = data.get('date').split('-')
        return {
            'year': date[0],
            'month': data[1],
            'day': data[2]
        }

    def to_representation(self, node):
        return node.id

    def create(self, validated_data):
        return NodeDate(**validated_data).save()
