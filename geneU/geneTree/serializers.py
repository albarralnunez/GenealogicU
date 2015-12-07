
from rest_framework import serializers
from .models import Person
from geoencoding_node_structure.serializers import LocationSerializer
from date_node_structure.serializers import DateSerializer
from date_node_structure.core import NodeDate
from geoencoding_node_structure.core import Location
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
        son_of = data.get('son_of')
        sons = data.get('sons')
        adopted = data.get('adopted')
        adopted_by = data.get('adopted_by')
        married = data.get('married')
        divorced = data.get('divorced')

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

        if son_of and son_of is not type(list):
            raise ValidationError({
                'son_of': "Incorrect data format, should be a list"
            })

        if sons and sons is not type(list):
            raise ValidationError({
                'sons': "Incorrect data format, should be a list"
            })

        if divorced and divorced is not type(list):
            raise ValidationError({
                'divorced': "Incorrect data format, should be a list"
            })

        if adopted and adopted is not type(list):
            raise ValidationError({
                'adopted': "Incorrect data format, should be a list"
            })

        if adopted_by and adopted_by is not type(list):
            raise ValidationError({
                'adopted_by': "Incorrect data format, should be a list"
            })

        if married and married is not type(list):
            raise ValidationError({
                'married': "Incorrect data format, should be a list"
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
            'born_in': born_in,
            'death_in': death_in,
            'lived_in': lived_in,
            'son_of': son_of,
            'sons': sons,
            'adopted': adopted,
            'adopted_by': adopted_by,
            'married': married,
            'divorced': divorced
        }

    def to_representation(self, node):

        if self.simple:
            return {
                'id': node.id
            }

        sons = list(node.sons.all())
        sons_serialized = None
        if sons:
            sons_serialized = PersonSerializer(
                sons, many=True, simple=True).data

        son_of = list(node.son_of.all())
        son_of_serialized = None
        if son_of:
            son_of_serialized = PersonSerializer(
                son_of, many=True, simple=True).data

        adopted = list(node.adopted.all())
        adopted_serialized = None
        if adopted:
            sons_serialized = PersonSerializer(
                adopted, many=True, simple=True).data

        adopted_by = list(node.adopted_by.all())
        adopted_by_serialized = None
        if adopted_by:
            adopted_by_serialized = PersonSerializer(
                adopted_by, many=True, simple=True).data

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
            lived_in_serialized = LocationSerializer(
                lived_in, many=True).data

        death_date = list(node.death_date.all())
        death_date_serialized = None
        if death_date:
            death_date_serialized = DateSerializer(death_date[0]).data

        birth_date = list(node.birth_date.all())
        birth_date_serialized = None
        if birth_date:
            birth_date_serialized = DateSerializer(birth_date[0]).data

        married = list(node.married.all())
        married_serialized = None
        if married:
            married_serialized = PersonSerializer(
                married, many=True, simple=True).data

        divorced = list(node.divorced.all())
        divorced_serialized = None
        if divorced:
            divorced_serialized = PersonSerializer(
                divorced, many=True, simple=True).data

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
            'adopted': adopted_serialized,
            'adopted_by': adopted_by_serialized,
            'born_in': born_in_serialized,
            'death_in': death_in_serialized,
            'lived_in': lived_in_serialized,
            'married': married_serialized,
            'divorced': divorced_serialized
        }

    def create(self, validated_data):
        birth_date = validated_data.pop('birth_date')
        death_date = validated_data.pop('death_date')
        son_of = validated_data.pop('son_of', [])
        sons = validated_data.pop('sons', [])
        adopted = validated_data.pop('adopted', [])
        adopted_by = validated_data.pop('adopted_by', [])
        married = validated_data.pop('married', [])
        divorced = validated_data.pop('divorced', [])
        born_in = validated_data.pop('born_in')
        death_in = validated_data.pop('death_in')
        lived_in = validated_data.pop('lived_in', [])

        result = Person(**validated_data).save()

        if birth_date:
            bd = NodeDate(birth_date).save()
            result.birth_date.connect(bd)

        if death_date:
            dd = NodeDate(death_date).save()
            result.death_date.connect(dd)

        for father in son_of:
            result.son_of.connect(father)

        for son in sons:
            result.sons.connect(son)

        for ad in adopted:
            result.adopted.connect(ad)

        for ad_by in adopted_by:
            result.adopted_by.connect(ad_by)

        for m in married:
            result.marry(m)

        for p in divorced:
            result.divorce(p)

        if born_in:
            loc = Location(address_components=born_in).save()
            result.born_in.connect(loc)

        if death_in:
            loc = Location(address_components=death_in).save()
            result.death_in.connect(loc)

        for location in lived_in:
            loc = Location(address_components=location).save()
            result.lived_in.connect(loc)

        return result

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.second_surname = validated_data.get(
            'second_surname', instance.second_surname)
        instance.genere = validated_data.get('genere', instance.genere)

        birth_date = validated_data.get('birth_date')
        death_date = validated_data.get('death_date')
        sons = validated_data.get('sons', [])
        son_of = validated_data.get('son_of', [])
        born_in = validated_data.get('born_in')
        death_in = validated_data.get('death_in')
        lived_in = validated_data.get('lived_in', [])
        divorced = validated_data.get('divorced', [])
        married = validated_data.get('married', [])
        adopted = validated_data.get('adopted', [])
        adopted_by = validated_data.get('adopted_by', [])

        if birth_date:
            instance.set_birth_date(birth_date)

        if death_date:
            instance.set_death_date(death_date)

        instance.add_sons(sons)

        instance.add_sons_of(son_of)

        if born_in:
            instance.set_born_in(born_in)

        if death_in:
            instance.set_death_in(death_in)

        instance.add_lived_in(lived_in)

        instance.add_divorced(divorced)

        instance.add_married(married)

        instance.add_married(adopted)

        instance.add_adopted_by(adopted_by)

        res = instance.refresh()
        return res
