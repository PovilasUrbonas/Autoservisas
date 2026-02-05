from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Service, Order, Car, OrderLine
from django.core.paginator import Paginator
from django.db.models import Q


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
    q = request.GET.get("q", "").strip()

    cars_qs = Car.objects.all().order_by("make", "model", "license_plate")

    if q:
        cars_qs = cars_qs.filter(
            Q(client_name__icontains=q) |
            Q(make__icontains=q) |
            Q(model__icontains=q) |
            Q(license_plate__icontains=q) |
            Q(vin_code__icontains=q)
        )

    paginator = Paginator(cars_qs, 5)  # ← kiek automobilių puslapyje
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "q": q,
    }
    return render(request, "cars.html", context)


def car_detail(request, pk: int):
    car = get_object_or_404(Car, pk=pk)
    return render(request, "car_detail.html", {"car": car})


# -------------------------
# B) 2 klasės užsakymams
# -------------------------
class OrderListView(ListView):
    model = Order
    template_name = "order_list.html"
    context_object_name = "orders"
    ordering = ["-date"]
    paginate_by = 5


class OrderDetailView(DetailView):
    model = Order
    template_name = "order_detail.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lines"] = self.object.lines.select_related("service")
        return context
