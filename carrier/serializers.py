from rest_framework import serializers
from carrier.models import Order

class OrderSerializer(serializers.ModelSerializer):
    truck_name = serializers.CharField(source='truck.name', read_only=True)
    freight_route = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'status', 'bid', 'bid_price', 'truck_name', 'freight_route']

    def get_freight_route(self, obj):
        return f"{obj.freight.origin} → {obj.freight.destination}" if obj.freight else "-"
