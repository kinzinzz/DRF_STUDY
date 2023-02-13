from rest_framework import serializers
from .models import Check_list

class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check_list
        fields = ['id', 'content', 'place', 'stuff_list']

class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = '__all__'