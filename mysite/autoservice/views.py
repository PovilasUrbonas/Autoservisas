from django.shortcuts import render
from .models import Service, Order, Car

def index(request):
    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    context = {
        "services_count": Service.objects.count(),
        "cars_count": Car.objects.count(),
        "done_orders_count": Order.objects.filter(status="c").count(),
    }
    return render(request, template_name="index.html", context=context)