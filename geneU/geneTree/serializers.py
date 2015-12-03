from rest_framework import serializers
from datetime import datetime
from .models import Person
from geoencoding_node_structure.serializers import LocationSerializer
from date_node_structure.serializers import DateSerializer

from django.core.exceptions import ValidationError 


class PersonSerializer(serializers.BaseSerializer):
    
    def __init__(self, *args, **kwargs):

        self.simple = kwargs.pop('simple', False)
        super(PersonSerializer, self).__init__(*args, **kwargs)
        
    def to_internal_value(self, data):

        name = data.get('name')
        surname = data.get('surname')
        second_surname = data.get('second_surname')
        genere = data.get('genere')
        birth_date = data.get('birth_date')
        death_date = data.get('death_date')
        born_in = data.get('born_in')
        death_in = data.get('death_in')
        lived_in = data.get('lived_in')

        # Perform the data validation.
        if not name:
            raise ValidationError({
                'name': 'This field is required.'
            })
        if not genere:
            raise ValidationError({
                'genere': 'This field is required.'
            })
        if genere != 'M' and genere != 'W':
            raise ValidationError({
                'genere': "Incorrect data format, should be 'M' or 'W'"
            })

        # Return the validated values. This will be available as
        # the `.validated_data` property.
        return {
            'name': name,
            'surname': surname,
            'second_surname': second_surname,
            'genere': genere,
            'birth_date': birth_date,
            'death_date': death_date,
            'born_in' : born_in,
            'death_in' : death_in,
            'lived_in' : lived_in
        }

    def to_representation(self, node):

        if self.simple:
            return {
                'id': node.id
            }

        sons = list(node.sons.all())
        sons_serialized = None
        if sons:
            sons_serialized = PersonSerializer(sons, many=True, simple=True).data

        son_of = list(node.son_of.all())
        son_of_serialized = None
        if son_of:
            son_of_serialized = PersonSerializer(sons, many=True, simple=True).data

        born_in = list(node.born_in.all())
        born_in_serialized = None
        if born_in:
            born_in_serialized = LocationSerializer(born_in[0]).data

        death_in = list(node.death_in.all())
        death_in_serialized = None
        if death_in:
            death_in_serialized = LocationSerializer(death_in[0]).data

        lived_in = list(node.lived_in.all())
        lived_in_serialized = None
        if lived_in:
            lived_in_serialized = LocationSerializer(lived_in, many=True).data                

        death_date = list(node.death_date.all())
        death_date_serialized = None
        if death_date:
            death_date_serialized = DateSerializer(death_date[0]).data

        birth_date = list(node.birth_date.all())
        birth_date_serialized = None
        if birth_date:
            birth_date_serialized = DateSerializer(birth_date[0]).data

        return {
            'id': node.id,
            'name': node.name,
            'surname': node.surname,
            'second_surname': node.second_surname,
            'genere': node.genere,
            'birth_date': birth_date_serialized,
            'death_date': death_date_serialized,
            'sons': sons_serialized,
            'son_of': son_of_serialized,
            'born_in' : born_in_serialized,
            'death_in' : death_in_serialized,
            'lived_in' : lived_in_serialized
        }

    def create(self, validated_data):
        return Person(**validated_data).save()

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.second_surname = validated_data.get(
            'second_surname', instance.second_surname)
        instance.genere = validated_data.get('genere', instance.genere)
        instance.birth = validated_data.get('birth', instance.birth)
        instance.death = validated_data.get('death', instance.death)
        return instance

"""
class CountrySerializer(serializers.BaseSerializer):
    
    def to_internal_value(self, data):
        code = data.get('code')

        # Perform the data validation.
        if not code:
            raise ValidationError({
                'code': 'This field is required.'
            })
       
        # Return the validated values. This will be available as
        # the `.validated_data` property.
        return {
            'code': code,
            }

    def to_representation(self, node):
        return {
            'code': node.code,
        }

    def create(self, validated_data):
        return Contry(**validated_data).save()
"""