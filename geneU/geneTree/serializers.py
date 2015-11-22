from rest_framework import serializers, reverse
from datetime import datetime
from .models import Person, Country
from core.url_builder import UrlBuilder
from geneU.settings import HOSTNAME
#from django.core.urlresolvers import reverse


class PersonSerializer(serializers.BaseSerializer):
    
    def __init__(self, *args, **kwargs):
        self.simple = kwargs.pop('simple', False)
        super(PersonSerializer, self).__init__(*args, **kwargs)
        
    def to_internal_value(self, data):
        name = data.get('name')
        surname = data.get('surname')
        second_surname = data.get('second_surname')
        genere = data.get('genere')
        birth = data.get('birth')
        death = data.get('death')

        # Perform the data validation.
        if not name:
            raise ValidationError({
                'name': 'This field is required.'
            })
        if not surname:
            raise ValidationError({
                'surname': 'This field is required.'
            })
        if genere != 'M' or genere != 'W':
            raise ValidationError({
                'genere': "Incorrect data format, should be 'M' or 'W'"
            })
        try:
            birth_date = datetime.strptime(birth, '%Y-%m-%d')
        except ValidationError:
            raise ValidationError("Incorrect data format, should be YYYY-MM-DD")
        try:
            death_date = datetime.strptime(death, '%Y-%m-%d')
        except ValidationError:
            raise ValidationError("Incorrect data format, should be YYYY-MM-DD")

        # Return the validated values. This will be available as
        # the `.validated_data` property.
        return {
            'name': name,
            'surname': surname,
            'second_surname': second_surname,
            'genere': genere,
            'birth': birth_date,
            'death': death_date,
        }

    def to_representation(self, node):
        country = list(node.country.all())
        country_serialized = None
        if country:
            country_serialized = CountrySerializer(country[0]).data

        sons = list(node.sons.all())
        sons_serialized = None
        if sons:
            sons_serialized = PersonSerializer(sons, many=True, simple=True).data
        
        son_of = list(node.son_of.all())
        son_of_serialized = None
        if son_of:
            son_of_serialized = PersonSerializer(sons, many=True, simple=True).data


        if self.simple:
            return {
                'id': node.id
            }

        return {
            'id': node.id,
            'name': node.name,
            'surname': node.surname,
            'second_surname': node.second_surname,
            'genere': node.genere,
            'birth': node.birth,
            'death': node.death,
            'country': country_serialized,
            'sons': sons_serialized,
            'son_of': son_of_serialized
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
