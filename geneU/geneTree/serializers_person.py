from geoencoding_node_structure.serializers import LocationSerializer
from date_node_structure.serializers import DateSerializer
import geneTree.models_person as models_person
from rest_framework import serializers
from django.core.exceptions import ValidationError
from datetime import datetime
from django.core.urlresolvers import reverse


class EventSerializer(serializers.BaseSerializer):

    def to_internal_value(self, data):
        location = data.get('location')
        date_begin = data.get('date_beging')
        date_end = data.get('date_end')
        descritive_location = data.get('descritive_location')
        description = data.get('description')

        if date_begin:
            try:
                date_begin = datetime.strptime(
                    date_begin, "%Y-%m-%d")
            except(ValidationError):
                raise ValidationError({
                    'date_begin': "Incorrect data format," +
                    " the date format should be YYYY-MM-DD"
                })
        if date_end:
            try:
                date_end = datetime.strptime(
                    date_end, "%Y-%m-%d")
            except(ValidationError):
                raise ValidationError({
                    'date_end': "Incorrect data format," +
                    " the date format should be YYYY-MM-DD"
                })
        return {
            'loc': location,
            'date_begin': date_begin,
            'date_end': date_end,
            'location_prop': descritive_location,
            'description': description
        }

    def to_representation(self, node):
        location = list(node.location.all())
        location_serialized = None
        if location:
            location_serialized = LocationSerializer(location[0]).data
        date_begin = list(node.date_begin.all())
        date_begin_serialized = None
        if date_begin:
            date_begin_serialized = DateSerializer(date_begin[0]).data
        date_end = list(node.date_end.all())
        date_end_serialized = None
        if date_end:
            date_end_serialized = DateSerializer(date_end[0]).data
        return {
            'location': location_serialized,
            'date_begin': date_begin_serialized,
            'date_end': date_end_serialized,
            'descritive_location': node.location_prop,
            'description': node.description
        }


class MarriageSerializer(EventSerializer):

    def to_internal_value(self, data):
        if data['spouse1']:
            spouse1 = data.pop('spouse1')
        if data['spouse2']:
            spouse2 = data.pop('spouse2')

        validated_data = \
            super(MarriageSerializer, self).to_internal_value(data)
        validated_data['spouse1'] = models_person.Person.nodes.get(id=spouse1)
        validated_data['spouse2'] = models_person.Person.nodes.get(id=spouse2)
        if not spouse1 and not spouse2:
            raise ValidationError({
                'spouse': "At least one spouse must be supplied"
            })
        return validated_data

    def to_representation(self, node):
        representation = \
            super(MarriageSerializer, self).to_representation(node)
        married = node.get_spouses()
        married_serialized = None
        if married:
            married_serialized = PersonSerializer(
                married, many=True, simple=True).data
        representation['spouses'] = married_serialized
        representation['url'] = reverse(
            'marriage-detail',
            kwargs={'id': node.id}
        )
        return representation

    def create(self, validated_data):
        m = models_person.Marriage().save()
        if validated_data['spouse2']:
            spouse2 = validated_data.pop('spouse2')
            m.add_spouse(spouse2)
        if validated_data['spouse1']:
            spouse1 = validated_data.pop('spouse1')
            m.add_spouse(spouse1)
        m.set_event(**validated_data)
        return m


class DivorceSerializer(EventSerializer):

    def to_internal_value(self, data):
        if data['spouse1']:
            spouse1 = data.pop('spouse1')
        if data['spouse2']:
            spouse2 = data.pop('spouse2')

        validated_data = \
            super(DivorceSerializer, self).to_internal_value(data)
        validated_data['spouse1'] = models_person.Person.nodes.get(id=spouse1)
        validated_data['spouse2'] = models_person.Person.nodes.get(id=spouse2)
        if not spouse1 and not spouse2:
            raise ValidationError({
                'spouse': "At least one spouse must be supplied"
            })
        return validated_data

    def to_representation(self, node):
        representation = \
            super(DivorceSerializer, self).to_representation(node)
        divorced = node.get_spouses()
        divorced_serialized = None
        if divorced:
            divorced_serialized = PersonSerializer(
                divorced, many=True, simple=True).data
        representation['spouses'] = divorced_serialized
        representation['url'] = reverse(
            'divorce-detail',
            kwargs={'id': node.id}
        )
        return representation

    def create(self, validated_data):
        m = models_person.Divorce().save()
        if validated_data['spouse2']:
            spouse2 = validated_data.pop('spouse2')
            m.add_spouse(spouse2)
        if validated_data['spouse1']:
            spouse1 = validated_data.pop('spouse1')
            m.add_spouse(spouse1)
        m.set_event(**validated_data)
        return m


class BirthSerializer(EventSerializer):

    def to_internal_value(self, data):
        if data['father1']:
            father1 = data.pop('father1')
        if data['father2']:
            father2 = data.pop('father2')
        son = data.get('son')
        if not son:
            raise ValidationError({
                'son': "atribute is required"
            })
        validated_data = \
            super(BirthSerializer, self).to_internal_value(data)
        validated_data['father1'] = models_person.Person.nodes.get(id=father1)
        validated_data['father2'] = models_person.Person.nodes.get(id=father2)
        validated_data['son'] = models_person.Person.nodes.get(id=son)
        return validated_data

    def to_representation(self, node):
        representation = \
            super(BirthSerializer, self).to_representation(node)
        son = node.get_son()
        son_serialized = PersonSerializer(son, simple=True).data
        representation['son'] = son_serialized
        fathers = node.get_fathers()
        fathers_serialized = None
        if fathers:
            fathers_serialized = PersonSerializer(
                fathers, many=True, simple=True).data
        representation['url'] = reverse(
            'birth-detail',
            kwargs={'id': node.id}
        )
        representation['fathers'] = fathers_serialized
        return representation

    def create(self, validated_data):
        m = models_person.Birth().save()
        if validated_data['father2']:
            father2 = validated_data.pop('father2')
            m.add_father(father2)
        if validated_data['father1']:
            father1 = validated_data.pop('father1')
            m.add_father(father1)
        son = validated_data.pop('son')
        m.set_son(son)
        m.set_event(**validated_data)
        return m


class DeathSerializer(EventSerializer):

    def to_internal_value(self, data):
        death = data.get('death')
        if not death:
            raise ValidationError({
                'death': "atribute is required"
            })
        validated_data = \
            super(DeathSerializer, self).to_internal_value(data)
        validated_data['death'] = models_person.Person.nodes.get(id=death)
        return validated_data

    def to_representation(self, node):
        representation = \
            super(DeathSerializer, self).to_representation(node)
        d = node.get_person()
        death_serialized = PersonSerializer(d, simple=True).data
        representation['person'] = death_serialized
        representation['url'] = reverse(
            'death-detail',
            kwargs={'id': node.id}
        )
        return representation

    def create(self, validated_data):
        m = models_person.Death().save()
        death = validated_data.pop('death')
        m.set_death(death)
        m.set_event(**validated_data)
        return m


class AdoptionSerializer(EventSerializer):

    def to_internal_value(self, data):
        if data['father1']:
            father1 = data.pop('father1')
        if data['father2']:
            father2 = data.pop('father2')
        son = data.get('son')
        if not son:
            raise ValidationError({
                'son': "atribute is required"
            })
        validated_data = \
            super(AdoptionSerializer, self).to_internal_value(data)
        validated_data['father1'] = models_person.Person.nodes.get(id=father1)
        validated_data['father2'] = models_person.Person.nodes.get(id=father2)
        validated_data['son'] = models_person.Person.nodes.get(id=son)
        return validated_data

    def to_representation(self, node):
        representation = \
            super(AdoptionSerializer, self).to_representation(node)
        son_serialized = PersonSerializer(node.get_son(), simple=True).data
        representation['son'] = son_serialized
        fathers = node.get_fathers()
        fathers_serialized = None
        if fathers:
            fathers_serialized = PersonSerializer(
                fathers, many=True, simple=True).data
        representation['fathers'] = fathers_serialized
        representation['url'] = reverse(
            'adoption-detail',
            kwargs={'id': node.id}
        )
        return representation

    def create(self, validated_data):
        m = models_person.Adoption().save()
        if validated_data['father2']:
            father2 = validated_data.pop('father2')
            m.add_father(father2)
        if validated_data['father1']:
            father1 = validated_data.pop('father1')
            m.add_father(father1)
        son = validated_data.pop('son')
        m.set_son(son)
        m.set_event(**validated_data)
        return m


class LivedSerializer(EventSerializer):

    def to_internal_value(self, data):
        if data['person']:
            person = data.pop('person')
        validated_data = \
            super(LivedSerializer, self).to_internal_value(data)
        validated_data['person'] = models_person.Person.nodes.get(id=person)
        if not person:
            raise ValidationError({
                'person': "atribute is required"
            })
        return validated_data

    def to_representation(self, node):
        representation = \
            super(LivedSerializer, self).to_representation(node)
        person = node.get_person()
        serialized = None
        if person:
            serialized = PersonSerializer(person, simple=True).data
        representation['person'] = serialized
        representation['url'] = reverse(
            'lived-detail',
            kwargs={'id': node.id}
        )
        return representation

    def create(self, validated_data):
        m = models_person.Lived().save()
        if validated_data['person']:
            person = validated_data.pop('person')
            m.set_person(person)
        m.set_event(**validated_data)
        return m


class PersonSerializer(serializers.BaseSerializer):

    def __init__(self, *args, **kwargs):
        self.simple = kwargs.pop('simple', False)
        super(PersonSerializer, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        name = data.get('name')
        surname = data.get('surname')
        second_surname = data.get('second_surname')
        genere = data.get('genere')
        tree = data.get('tree')

        if not tree:
            raise ValidationError({
                'Tree': "atribute is required"
            })

        tree = models_person.Tree.nodes.get(id=tree)

        return {
            'name': name,
            'surname': surname,
            'second_surname': second_surname,
            'gener': genere,
            'tree': tree
        }

    def to_representation(self, node):
        if self.simple:
            return reverse('person-detail', kwargs={'id': node.id})
        response = {}
        response['marriages'] = None
        response['divorces'] = None
        response['birth'] = None
        response['death'] = None
        response['adopted'] = None
        response['death'] = None
        response['adoptions'] = None
        response['father'] = None
        response['lived'] = None
        marriages = node.get_marriages()
        if marriages:
            response['marriages'] = MarriageSerializer(
                marriages, many=True).data
        divores = node.get_divorces()
        if divores:
            response['divorces'] = DivorceSerializer(divores, many=True).data
        adopted = node.get_adopted()
        if adopted:
            response['adopted'] = AdoptionSerializer(adopted).data
        birth = node.get_birth()
        if birth:
            response['birth'] = BirthSerializer(birth).data
        death = node.get_death()
        if death:
            response['death'] = DeathSerializer(death).data
        adoptions = node.get_adoptions()
        if adoptions:
            response['adoptions'] = AdoptionSerializer(
                adoptions, many=True).data
        father = node.get_father()
        if father:
            response['father'] = BirthSerializer(father, many=True).data
        lived = node.get_lived()
        if lived:
            response['lived'] = LivedSerializer(lived, many=True).data
        response['url'] = reverse('person-detail', kwargs={'id': node.id})
        response['name'] = node.name
        response['surname'] = node.surname
        response['second_surname'] = node.second_surname
        response['genere'] = node.genere
        return response

    def create(self, validated_data):
        tree = validated_data.pop('tree')
        p = models_person.Person(**validated_data).save()
        tree = tree if tree else self.tree
        p.set_tree(tree)
        return p
