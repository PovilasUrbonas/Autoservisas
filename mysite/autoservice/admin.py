from django.contrib import admin
from .models import Service, Car, Order, OrderLine


# Register your models here.

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    can_delete = False
    extra = 0
    fields = ['service', 'quantity', 'line_sum']
    readonly_fields = ['line_sum']

    @admin.display(description="Line sum")
    def line_sum(self, obj):
        if not obj.service or obj.quantity is None:
            return 0
        return obj.quantity * obj.service.price

class OrderAdmin(admin.ModelAdmin):
    list_display = ['car', 'date', 'status']
    # list_editable = ['status', 'user', 'deadline']
    inlines = [OrderLineInline]
    # fieldsets = [
    #     ("General", {'fields': ['car', 'date', 'status', 'user', 'deadline']}),
    # ]
    # readonly_fields = ['date', 'total']

class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'client_name', 'license_plate', 'vin_code']
    list_filter = ['client_name', 'make', 'model']
    search_fields = ['license_plate', 'vin_code']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['order', 'service', 'quantity', 'line_sum']
    fieldsets = [
        ("General", {'fields': ['order', 'service', 'quantity', 'line_sum']}),
    ]
    readonly_fields = ['line_sum']

    @admin.display(description="Line sum")
    def line_sum(self, obj):
        if not obj.service or obj.quantity is None:
            return 0
        return obj.quantity * obj.service.price

admin.site.register(Car, CarAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)