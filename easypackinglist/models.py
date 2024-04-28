import uuid
from django.db import models
from django.contrib.auth.models import User

class Trip(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    selected_template_name = models.CharField(max_length=100, blank=True, null=True)
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    image = models.CharField(max_length=255, default='images/trip_images/default_background.jpg')

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)  # Changed from ForeignKey to CharField
    trip = models.ForeignKey(Trip, related_name='items', on_delete=models.CASCADE)
    is_packed = models.BooleanField(default=False)

