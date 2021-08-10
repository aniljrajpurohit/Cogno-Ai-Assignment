from django.contrib import admin
from .models import Restaurant, OrderPlaced, Dishes

admin.site.register(Restaurant)
admin.site.register(OrderPlaced)
admin.site.register(Dishes)
