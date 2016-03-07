from models import UserNode, UserProfile
from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError
from phonenumbers import is_possible_number, parse
from geneTree.serializers import TreeSerializer
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        read_only_fields = ('id',)


class UserProfileSerializer(serializers.BaseSerializer):

    def __init__(self, *args, **kwargs):
        self.simple = kwargs.pop('simple', False)
        super(UserProfileSerializer, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        internal = {}
        internal['phone_number'] = data.get('phone_number')
        internal['private'] = data.get('private')

        if internal['phone_number']:
            phonenumber = parse(internal['phone_number'], None)
            if not is_possible_number(phonenumber):
                raise ValidationError({
                    'phone_number': "phone_number is not valid"
                    })
        if internal['private']:
            internal['private'] = internal['private'] == 'True'
        ret = {}
        for x in internal:
            if internal[x]:
                ret[x] = internal[x]
        return ret

    def to_representation(self, obj):
        if self.simple:
            return '/user/{id}'.format(id=obj.id)
        res = {
            'url': '/user/{id}'.format(id=obj.id),
            'username': obj.user.username,
            'email': obj.user.email,
            'phone_number': obj.phone_number,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'trees': []
        }
        trees = UserNode.nodes.get(id=obj.user.id).own.all()
        if trees:
            res['trees'] = TreeSerializer(trees, many=True).data
        return res
    '''
    def create(self, validated_data):
        u = UserProfile.create_user(**validated_data)
        return u
    '''

    @transaction.atomic
    def update(self, obj, validated_data):
        obj.user.username = validated_data['username']
        obj.user.email = validated_data['email']
        obj.user.set_password(validated_data['password'])
        obj.user.first_name = validated_data['first_name']
        obj.user.last_name = validated_data['last_name']
        obj.user.save()
        obj.phone_number = validated_data['phone_number']
        obj.save()
        return obj.save()
