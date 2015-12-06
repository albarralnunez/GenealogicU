from .core import Location
from rest_framework import serializers
import json


class LocationSerializer(serializers.BaseSerializer):

    def to_internal_value(self, data):

        data = json.loads(data)

        return {
            'address': data
        }

    def to_representation(self, node):
        return {
            'formatted_address': node.formatted_address,
            'address': node.address
        }

    def create(self, validated_data):
        return Location(**validated_data).save()
