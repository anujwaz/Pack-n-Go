from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  

# Create your models here.

class booking(models.Model):
    
    type = (('pune', 'pune'), ('mumbai', 'mumbai'), ('agra','agra'), ('beed', 'beed'), ('solapur', 'solapur'),
           ('banglore', 'banglore'), ('delhi', 'delhi'), ('mirzapur', 'mirzapur'), ('jaunpur', 'jaunpur'))
    
    type_1 = (('0-20', '0-20'), ('20-40', '20-40'), ('40-60', '40-60'))
    
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    quantity = models.CharField(max_length=200, choices=type_1)
    price = models.IntegerField(default=0)
    pickup_loc = models.CharField(max_length=200, choices=type)
    drop_loc = models.CharField(max_length=200, choices=type)
    phone_no = models.IntegerField()
    name = models.CharField(max_length=200)
    vehicle = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name} - {self.vehicle}'
    
class Driver(models.Model):
    name = models.CharField(max_length=200)
    contact_info = models.CharField(max_length=200)
    vehicle_info = models.CharField(max_length=200)
    availability_status = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    

    