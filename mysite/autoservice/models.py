from django.db import models

# Create your models here.

class Car(models.Model):
    make = models.CharField(verbose_name="Make", max_length=100)
    model = models.CharField(verbose_name="Model", max_length=100)
    license_plate = models.CharField(verbose_name="License Plate", max_length=10)
    vin_code = models.CharField(verbose_name="VIN Code", max_length=20)
    client_name = models.CharField(verbose_name="Client Name", max_length=500)
    photo = models.ImageField('Photo', upload_to='car', null=True, blank=True)
    description = HTMLField(verbose_name="Description", max_length=3000, default="")

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Paslauga")
    price = models.DecimalField(verbose_name="Kaina", max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"

class Order(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name="Data")
    car = models.ForeignKey(to="Car", verbose_name="Automobilis", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.car} ({self.date})"

class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE, verbose_name="Užsakymas")
    service = models.ForeignKey(to="Service", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Paslauga")
    quantity = models.PositiveIntegerField(verbose_name="Kiekis", default=1)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return f"{self.order} x{self.quantity}"