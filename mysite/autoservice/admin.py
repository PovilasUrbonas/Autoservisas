from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Service, Car, Order, OrderLine, OrderReview, CustomUser


# CustomUser admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'photo']
    fieldsets = UserAdmin.fieldsets + (
        ('Papildoma informacija', {'fields': ('photo',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Papildoma informacija', {'fields': ('photo',)}),
    )


# Register your models here.

class OrderLineInLine(admin.TabularInline):
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
    list_display = ['car', 'date', 'user', 'due_back', 'status', 'total']
    list_editable = ['status', 'user', 'due_back']
    inlines = [OrderLineInLine]
    readonly_fields = ['date', 'total']

    fieldsets = [
        ("General", {'fields': ['car', 'date', 'user', 'due_back', 'status', 'total']}),
    ]


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'client_name', 'license_plate', 'vin_code', 'photo']
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

class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ['order', 'date_created', 'reviewer', 'content']

admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
admin.site.register(OrderReview, OrderReviewAdmin)