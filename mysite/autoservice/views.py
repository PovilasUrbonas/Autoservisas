from django.shortcuts import render
from .models import Service, Order, Car


def index(request):
    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_services": Service.objects.count(),
        "num_orders_done": Order.objects.filter(status="c").count(),
        "num_cars": Car.objects.count(),
        "num_visits": num_visits,
    }
    return render(request, template_name="index.html", context=context)