from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from tinymce.models import HTMLField
from PIL import Image
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    photo = models.ImageField(verbose_name=_("Photo"), upload_to="profile_pics", null=True, blank=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            min_side = min(img.width, img.height)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side
            img = img.crop((left, top, right, bottom))
            img = img.resize((300, 300), Image.LANCZOS)
            img.save(self.photo.path)


class Car(models.Model):
    make = models.CharField(verbose_name=_("Make"), max_length=100)
    model = models.CharField(verbose_name=_("Model"), max_length=100)
    license_plate = models.CharField(verbose_name=_("License Plate"), max_length=10)
    vin_code = models.CharField(verbose_name=_("VIN Code"), max_length=20)
    client_name = models.CharField(verbose_name=_("Client Name"), max_length=500)
    photo = models.ImageField(verbose_name=_("Photo"), upload_to='car', null=True, blank=True)
    description = HTMLField(verbose_name=_("Description"), max_length=3000, default="")

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

    def display_vin_code(self):
        return self.vin_code

    display_vin_code.short_description = _("VIN Code")

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")


class Service(models.Model):
    name = models.CharField(verbose_name=_("Service"), max_length=100)
    price = models.FloatField(verbose_name=_("Price"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")


class Order(models.Model):
    date = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)
    car = models.ForeignKey(to="Car", verbose_name=_("Car"), on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(to="CustomUser", verbose_name=_("User"), on_delete=models.SET_NULL, null=True, blank=True)
    due_back = models.DateField(verbose_name=_("Due Back"), null=True, blank=True)

    ORDER_STATUS = (
        ('p', _('Pending')),
        ('i', _('In Progress')),
        ('c', _('Completed')),
        ('x', _('Cancelled')),
    )

    status = models.CharField(
        verbose_name=_("Status"),
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
        if self.due_back and timezone.now().date() > self.due_back:
            return True
        return False

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE, related_name="lines", verbose_name=_("Order"))
    service = models.ForeignKey(to="Service", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Service"))
    quantity = models.IntegerField(verbose_name=_("Quantity"), default=1)

    def line_sum(self):
        if self.service is None:
            return 0
        return self.quantity * self.service.price

    line_sum.short_description = _("Line Sum")

    class Meta:
        verbose_name = _("Order Line")
        verbose_name_plural = _("Order Lines")


class OrderReview(models.Model):
    order = models.ForeignKey(to="Order", verbose_name=_("Order"), on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews")
    reviewer = models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name=_("Reviewer"), on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(verbose_name=_("Date Created"), auto_now_add=True)
    content = models.TextField(verbose_name=_("Content"), max_length=2000)

    class Meta:
        verbose_name = _("Order Review")
        verbose_name_plural = _("Order Reviews")
        ordering = ['-date_created']
