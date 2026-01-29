from django.contrib import admin
from .models import Service, Car, Order, OrderLine

class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'license_plate']

admin.site.register(Service)
admin.site.register(Car, CarAdmin)
admin.site.register(Order)
admin.site.register(OrderLine)