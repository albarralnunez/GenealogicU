from rest_framework import serializers
from django.core.exceptions import ValidationError
from datetime import datetime


class DateSerializer(serializers.BaseSerializer):

    def to_internal_value(self, date):

        if not date:
            raise ValidationError({
                'date': 'This field is required.'
            })
        date = datetime.strptime(date, '%Y-%m-%d')
        print date
        return {
            'date': date
        }

    def to_representation(self, node):
        return node.id
