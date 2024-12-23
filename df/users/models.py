# users/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions_set')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    teleg = models.CharField(max_length=50,blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

