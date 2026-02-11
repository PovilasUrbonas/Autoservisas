from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Service, Order, Car, OrderLine
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy
from .forms import OrderReviewForm, CustomUserChangeForm, CustomUserCreationForm, InstanceCreateUpdateForm
from django.views.generic.edit import FormMixin
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def index(request):
    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    context = {
        "services_count": Service.objects.count(),
        "cars_count": Car.objects.count(),
        "done_orders_count": Order.objects.filter(status="c").count(),
        "num_visits": num_visits,
    }
    return render(request, "index.html", context=context)

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

class OrderDetailView(FormMixin, DetailView):
    model = Order
    template_name = "order_detail.html"
    context_object_name = "order"
    form_class = OrderReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lines"] = self.object.lines.select_related("service")
        context["reviews"] = self.object.reviews.all()
        return context

    # nurodome, kur atsidursime komentaro sėkmės atveju.
    def get_success_url(self):
        return reverse("autoservice:order-detail", kwargs={"pk": self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # nurodome, kad užsakymas bus tas, po kuriuo komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        form.instance.order = self.get_object()
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)

class MyOrdersListView(LoginRequiredMixin, ListView):
    """Prisijungusio vartotojo užsakymų sąrašas"""
    model = Order
    template_name = "my_orders.html"
    context_object_name = "orders"
    paginate_by = 5

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-date")


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = CustomUserChangeForm
    template_name = "profile.html"
    success_url = reverse_lazy('autoservice:profile')

    def get_object(self, queryset=None):
        return self.request.user

class OrderInstanceDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = OrderInstance
    context_object_name = "instance"
    template_name = "instance.html"

    def test_func(self):
        return self.request.user.is_staff

class OrderInstanceCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = OrderInstance
    template_name = "instance_form.html"
    form_class = InstanceCreateUpdateForm
    # fields = ['car', 'user', 'due_back', 'status', 'order']
    success_url = reverse_lazy('instances')

    def test_func(self):
        return self.request.user.is_staff