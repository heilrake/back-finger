from django.db import models


# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    user_finger_img = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name