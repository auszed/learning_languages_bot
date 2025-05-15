from django.db import models

# Create your models here.
class NewUserAccount(models.Model):
    """model for creating users"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    terms_agreement = models.BooleanField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"