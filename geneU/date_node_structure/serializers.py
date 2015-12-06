from .core import NodeDate
from rest_framework import serializers
from django.core.exceptions import ValidationError


class DateSerializer(serializers.BaseSerializer):

    def to_internal_value(self, date):

        if not date:
            raise ValidationError({
                'date': 'This field is required.'
            })

        try:
            date = date.split('-')
            if len(date[2]) < 2:
                raise ValidationError(
                    "Incorrect data format, should be YYYY-MM-DD")
            elif len(date[1]) < 2:
                raise ValidationError(
                    "Incorrect data format, should be YYYY-MM-DD")
            elif len(date[0]) < 4:
                raise ValidationError(
                    "Incorrect data format, should be YYYY-MM-DD")

            return {
                'year': int(date[0]),
                'month': int(date[1]),
                'day': int(date[2])
            }

        except ValidationError:
            raise ValidationError(
                "Incorrect data format, should be YYYY-MM-DD")

    def to_representation(self, node):
        return node.id

    def create(self, validated_data):
        print validated_data
        return NodeDate(**validated_data).save()
