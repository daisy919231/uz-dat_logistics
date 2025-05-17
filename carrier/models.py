from django.db import models
from shipper.models import Freight, Location
from config import settings

# Create your models here.
class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class Driver(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name=models.CharField(max_length=200)
    phone_number=models.CharField(max_length=15, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.full_name

class Truck(BaseModel):
    class TypeChoices(models.TextChoices):
        type1='Flatbed'
        type2='Tank'
        type3='Dry van'
        type4='Box truck'
    type=models.CharField(choices=TypeChoices.choices, default=TypeChoices.type1)
    driver=models.ForeignKey(Driver, on_delete=models.CASCADE)
    truck_number=models.CharField(max_length=30, null=True)

    def __str__(self):
        return f'{self.type} {self.truck_number}'
    

class Order(BaseModel):
    class StatusChoices(models.TextChoices):
        complete='Complete'
        not_complete='Not Complete'
        
    status = models.CharField(choices=StatusChoices.choices, default=StatusChoices.complete)
    bid = models.BooleanField()
    bid_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    avto = models.CharField(max_length=200, null=True)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='orders')
    freight = models.ForeignKey(Freight, on_delete=models.CASCADE, related_name='orders')

    @property
    def final_price(self):
        if self.bid and self.bid_price:
            return self.bid_price
        return self.freight.offered_price
