from django.db import models


class Contact_Us_Login(models.Model):
    roll_no = models.CharField(max_length=10,primary_key=True)
    email = models.EmailField(default='')
    description = models.TextField(default='')
    def __str__(self):
        return self.roll_no
