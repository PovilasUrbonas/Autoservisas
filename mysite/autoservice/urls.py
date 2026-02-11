from django.urls import path
from . import views

# urlpatterns = [
#     path("", views.index, name="index"),
#
#     path("cars/", views.cars_list, name="cars_list"),
#     path("cars/<int:pk>/", views.car_detail, name="car_detail"),
#
#     path("orders/", views.OrderListView.as_view(), name="orders_list"),
#     path("orders/<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),
# ]

app_name = "autoservice"

urlpatterns = [
    path("", views.index, name="index"),

    # automobiliai (function-based)
    path("automobiliai/", views.cars_list, name="car-list"),
    path("automobiliai/<int:pk>/", views.car_detail, name="car-detail"),

    # uzsakymai (class-based)
    path("uzsakymai/", views.OrderListView.as_view(), name="order-list"),
    path("uzsakymai/<int:pk>/", views.OrderDetailView.as_view(), name="order-detail"),

    # mano uzsakymai
    path("manouzsakymai/", views.MyOrdersListView.as_view(), name="my-orders"),

    # prisijungimai
    path('signup/', views.SignUpView.as_view(), name='signup'),

    # profilis
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),

    path("instances/", views.OrderInstanceListView.as_view(), name="instances"),
    path("instances/<int:pk>", views.OrderInstanceDetailView.as_view(), name="instance")
    path("instances/create", views.OrderInstanceCreateView.as_view(), name="instance_create"),
]