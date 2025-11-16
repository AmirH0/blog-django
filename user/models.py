from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(max_length=3, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_data = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=True, null=True
    )
    craeted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}"
