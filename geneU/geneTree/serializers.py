from rest_framework import serializers
from datetime import datetime
from .models import Person

class PersonSerializer(serializers.BaseSerializer):
    
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
        return {
            'id': node.id,
            'name': node.name,
            'surname': node.surname,
            'second_surname': node.second_surname,
            'genere': node.genere,
            'birth': node.birth,
            'death': node.death
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