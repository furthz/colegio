from django.contrib.auth.models import User, Group
from rest_framework import serializers
from authtools.models import User as Userss


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Userss
        fields = ('id','name', 'email')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id','name')
