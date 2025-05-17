from rest_framework import serializers
from shipper.models import Freight, Location

class FreightSerializer(serializers.ModelSerializer):
    class Meta:
        model=Freight
        fields='__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Location
        fields='__all__'