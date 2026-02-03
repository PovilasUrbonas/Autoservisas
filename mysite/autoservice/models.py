from django.db import models

# Create your models here.

class Car(models.Model):
    make = models.CharField(verbose_name="Make", max_length=100)
    model = models.CharField(verbose_name="Model", max_length=100)
    license_plate = models.CharField(verbose_name="License Plate", max_length=10)
    vin_code = models.CharField(verbose_name="VIN Code", max_length=20)
    client_name = models.CharField(verbose_name="Client Name", max_length=500)
    # photo = models.ImageField('Photo', upload_to='car', null=True, blank=True)
    # description = HTMLField(verbose_name="Description", max_length=3000, default="")

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

    def display_vin_code(self):
        return self.vin_code

    display_vin_code.short_description = "VIN Code"

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

class Service(models.Model):
    name = models.CharField(verbose_name="Service", max_length=100)
    price = models.FloatField(verbose_name="Price")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

class Order(models.Model):
    date = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    car = models.ForeignKey(to="Car", on_delete=models.SET_NULL, null=True, blank=True)
    # users = models.ForeignKey(to="autoservice.CustomUser", verbose_name="User", on_delete=models.SET_NULL, null=True, blank=True)
    # deadline = models.DateField(verbose_name="Deadline", null=True, blank=True)

    ORDER_STATUS = (
        ('p', 'Pending'),
        ('i', 'In Progress'),
        ('c', 'Completed'),
        ('x', 'Cancelled'),
    )

    status = models.CharField(
        verbose_name="Status",
        max_length=1,
        choices=ORDER_STATUS,
        default='p')

    def __str__(self):
        return f"Order {self.date}: {self.car}"

    @property
    def total(self):
        return sum(line.line_sum() for line in self.lines.all())

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

from django.db import models

class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE, related_name="lines", verbose_name="lines")
    service = models.ForeignKey(to="Service", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(verbose_name="Quantity", default=1)

    def line_sum(self):
        if self.service is None:
            return 0
        return self.quantity * self.service.price

    line_sum.short_description = "Line sum"

    class Meta:
        verbose_name = 'Order Line'
        verbose_name_plural = 'Order Lines'