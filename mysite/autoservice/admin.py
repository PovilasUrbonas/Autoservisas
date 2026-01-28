from django.contrib import admin

# Register your models here.
from .models import Service, Car, Order, OrderLine

class ServiceAdmin(admin.ModelAdmin):
    list_display = []

admin.site.register(Service)
admin.site.register(Car)
admin.site.register(Order)
admin.site.register(OrderLine)