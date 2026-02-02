from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Service, Order, OrderLine, Car


def index(request):
    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    context = {
        "services_count": Service.objects.count(),
        "cars_count": Car.objects.count(),
        "done_orders_count": Order.objects.filter(status="c").count(),
        "num_visits": num_visits,
    }
    return render(request, "index.html", context)


# -------------------------
# A) 2 funkcijos automobiliams
# -------------------------
def cars_list(request):
    cars = Car.objects.all().order_by("make", "model", "license_plate")
    return render(request, "cars.html", {"cars": cars})


def car_detail(request, pk: int):
    car = get_object_or_404(Car, pk=pk)
    return render(request, "car_detail.html", {"car": car})


# -------------------------
# B) 2 klasės užsakymams
# -------------------------
class OrderListView(ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"
    ordering = ["-date"]


class OrderDetailView(DetailView):
    model = Order
    template_name = "order_detail.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lines"] = (
            OrderLine.objects.filter(order=self.object)
            .select_related("service")
            .order_by("id")
        )
        return context