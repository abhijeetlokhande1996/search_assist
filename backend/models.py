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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text_for_vector = models.TextField(default=None, null=True)
