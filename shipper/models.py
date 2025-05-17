from django.db import models
from config import settings
# Create your models here.

class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class Shipper(BaseModel):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name=models.CharField(max_length=200, null=True)
    phone_number=models.CharField(max_length=20, null=True)
    company_name=models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.full_name or 'Noname'

# class Location(BaseModel):
#     location1=models.CharField(max_length=250, null=True)
#     location2=models.CharField(max_length=250, null=True)
#     distance=models.PositiveIntegerField(default=0)

#     def display_location(self):
#         if hasattr(self, 'location1') and hasattr(self, 'location2'):
#             return f"{self.location1} - {self.location2}"
#         return str(self)  # fallback to __str__ method
    
#     def __str__(self):
#         return self.display_location()

class Freight(BaseModel):
    class StatusChoices(models.TextChoices):
        searching='Searching'
        booked='Booked'
    name=models.CharField(max_length=200, blank=True, null=True)
    shipper=models.ForeignKey(Shipper, on_delete=models.CASCADE, related_name='freights')
    trailer=models.PositiveIntegerField(default=0)
    mass=models.PositiveIntegerField(default=0)
    status=models.CharField(choices=StatusChoices.choices, default=StatusChoices.searching)
    origin=models.CharField(max_length=100, null=True)
    destination=models.CharField(max_length=100, null=True)
    distance=models.PositiveIntegerField(default=0)
    offered_price=models.FloatField() #per km
    comment=models.TextField(blank=True, null=True)

    @property
    def display_location(self):
        if hasattr(self, 'origin') and hasattr(self, 'destination'):
            return f"{self.origin} - {self.destination}"
        return str(self)

    def __str__(self):
        return self.name or ''




