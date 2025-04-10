from django.db import models
from apps.users.models import User

class Category(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default="#000000")  

    def __str__(self):
        return f"{self.name}"