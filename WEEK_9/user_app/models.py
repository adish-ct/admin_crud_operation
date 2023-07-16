from django.db import models


# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=50, unique=True)
    user_name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)

    def __str__(self):
        return self.name
