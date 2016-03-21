from .core import Location
from rest_framework import serializers


class LocationSerializer(serializers.BaseSerializer):

    def to_internal_value(self, data):

        place_id = data.get('place_id')
        comp = data.get('address_components')

        return {
            'address_components': comp,
            'place_id': place_id
        }

    def to_representation(self, node):
        return {
            'formatted_address': node.formatted_address,
            'address': node.address,
        }

    def create(self, validated_data):
        print validated_data
        return Location(**validated_data).save()
