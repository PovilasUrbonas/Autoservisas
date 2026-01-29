from django.contrib import admin
from .models import Service, Car, Order, OrderLine

class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'license_plate', 'display_vin_code']

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['order', 'service', 'quantity', 'line_sum']
    fieldsets = [
        ("General", {'fields': ['order', 'service', 'quantity', 'line_sum']}),
    ]
    readonly_fields = ['line_sum']

admin.site.register(Car, CarAdmin)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(OrderLine, OrderLineAdmin)