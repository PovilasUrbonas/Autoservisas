from django.shortcuts import render
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
    query = request.GET.get("q", "").strip()

    qs = Car.objects.all().order_by("make", "model", "license_plate")

    if query:
        qs = qs.filter(
            Q(client_name__icontains=query) |
            Q(make__icontains=query) |
            Q(model__icontains=query) |
            Q(license_plate__icontains=query) |
            Q(vin_code__icontains=query)
        )

    paginator = Paginator(qs, 5)  # ← kiek automobilių puslapyje
    page_number = request.GET.get("page")
    cars_page = paginator.get_page(page_number)

    context = {
        "cars": cars_page,
        "query": query,
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
    paginate_by = 5
    ordering = ["-date"]  # naujausi užsakymai pirmi

class OrderDetailView(DetailView):
    model = Order
    template_name = "order_detail.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lines"] = self.object.lines.select_related("service")
        return context
