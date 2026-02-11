from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from tinymce.models import HTMLField
from PIL import Image
from django.conf import settings

# Custom User modelis su nuotrauka
class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to="profile_pics", null=True, blank=True)

    class Meta:
        verbose_name = "Vartotojas"
        verbose_name_plural = "Vartotojai"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            # Padarome kvadratinę
            min_side = min(img.width, img.height)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side
            img = img.crop((left, top, right, bottom))
            # Sumažiname iki 300x300
            img = img.resize((300, 300), Image.LANCZOS)
            img.save(self.photo.path)

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
    user = models.ForeignKey(to="CustomUser", verbose_name="Vartotojas", on_delete=models.SET_NULL, null=True, blank=True)
    due_back = models.DateField(verbose_name="Grąžinimo terminas", null=True, blank=True)

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

    @property
    def is_overdue(self):
        """Grąžina True, jei grąžinimo terminas praėjo"""
        if self.due_back and timezone.now().date() > self.due_back:
            return True
        return False

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

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

class OrderReview(models.Model):
    order = models.ForeignKey(to="Order", verbose_name="Order", on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews")
    reviewer = models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name="Reviewer", on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    content = models.TextField(verbose_name="Content", max_length=2000)

    class Meta:
        verbose_name = "Order Review"
        verbose_name_plural = 'Order Reviews'
        ordering = ['-date_created']


