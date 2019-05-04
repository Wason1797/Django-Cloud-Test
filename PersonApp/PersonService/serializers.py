from rest_framework import serializers
from .models import Person


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('person_id', 'person_name', 'person_attributes')
