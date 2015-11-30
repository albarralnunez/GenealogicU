from .core import Location
from rest_framework import serializers


class LocationSerializer(serializers.BaseSerializer):

    def to_internal_value(self, data):

        address_components = data.get('address_components')
        return {
            'address' : response.results[0]
        }

    def to_representation(self, node):
        return {
            'formatted_address' : node.formatted_address,
            'address' : node.address
        }

    def create(self, validated_data):
        return Location(**validated_data).save()
