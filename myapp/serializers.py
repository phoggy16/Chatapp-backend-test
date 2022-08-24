from dataclasses import fields
from rest_framework import serializers
from .models import Group,Messages


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields='__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Messages
        fields='__all__'