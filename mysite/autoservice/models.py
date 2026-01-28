from django.db import models

# Create your models here.

class Service(models.Model):
    name = models.ForeignKey(Paslaugos, on_delete=models.CASCADE, verbose_name="Paslauga")
    price = models.DecimalField(verbose_name="Kaina", max_digits=10, decimal_places=2)

    def __str__(self):
        return {self.name}

class Car(models.Model):
    make = models.CharField(verbose_name="Markė", max_length=100)
    model = models.CharField(verbose_name="Modelis", max_length=100)
    license_plate = models.CharField(verbose_name="Valstybinis Numeris", max_length=6)
    vin_code = models.CharField(verbose_name="VIN Code", max_length=17, unique=True)
    client_name = models.CharField(verbose_name="Kliento Vardas", max_length=100)

    def __str__(self):
        return f"{self.make} {self.model} {self.license_plate} {self.vin_code} {self.client_name}"

class Order(models.Model):
    data = models.DateField(auto_now_add= True, verbose_name="Data")
    car_id = models.ForeignKey(to="Car", verbose_name="Automobilis", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.car_id} ({self.data})"

class OrderLine(models.Model):
    order_id = models.ForeignKey(to="Order", on_delete=models.CASCADE, verbose_name="Užsakymas")
    service = models.Foreignkey(to="Service", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.CharField(verbose_name="Kiekis", max_length=50)

    def __str__(self):
        return f"{self.order_id} {self.quantity}"

