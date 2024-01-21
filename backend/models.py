from django.db import models

# Create your models here.


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    price = models.FloatField()
    description = models.TextField()
    primary_colour = models.CharField(max_length=20)
