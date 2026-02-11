from django.urls import path
from . import views

app_name = "autoservice"

urlpatterns = [
    path("", views.index, name="index"),

    # automobiliai (function-based)
    path("automobiliai/", views.cars_list, name="car-list"),
    path("automobiliai/<int:pk>/", views.car_detail, name="car-detail"),

    # uzsakymai (class-based) - visi užsakymai
    path("uzsakymai/", views.OrderListView.as_view(), name="order-list"),
    path("uzsakymai/<int:pk>/", views.OrderDetailView.as_view(), name="order-detail"),

    # mano uzsakymai
    path("manouzsakymai/", views.MyOrdersListView.as_view(), name="my-orders"),

    # užsakymų CRUD
    path("uzsakymai/naujas/", views.OrderCreateView.as_view(), name="order-create"),
    path("uzsakymai/<int:pk>/redaguoti/", views.OrderUpdateView.as_view(), name="order-update"),
    path("uzsakymai/<int:pk>/trinti/", views.OrderDeleteView.as_view(), name="order-delete"),

    # užsakymo eilučių CRUD
    path("uzsakymai/<int:order_pk>/eilute/nauja/", views.OrderLineCreateView.as_view(), name="orderline-create"),
    path("eilute/<int:pk>/redaguoti/", views.OrderLineUpdateView.as_view(), name="orderline-update"),
    path("eilute/<int:pk>/trinti/", views.OrderLineDeleteView.as_view(), name="orderline-delete"),

    # prisijungimai
    path('signup/', views.SignUpView.as_view(), name='signup'),

    # profilis
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
]
