from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    rest_name = models.CharField(max_length=50, default='')
    rest_address = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.rest_name


class Dishes(models.Model):
    dish_name = models.CharField(max_length=50, default='')
    price = models.IntegerField(default=0)
    rest_name = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.dish_name


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rest_name = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    total_price = models.IntegerField(default=0)
    date = models.DateField()

    def __str__(self):
        return self.user.username
