from django.urls import path
from .views import (
    CreateOrderView,
    MyOrdersView,
    OrderDetailView,
    AdminOrderStatusUpdateView,
)

urlpatterns = [
    path("create/", CreateOrderView.as_view()),
    path("my-orders/", MyOrdersView.as_view()),
    path("<int:id>/", OrderDetailView.as_view()),
    path("<int:id>/admin-update/", AdminOrderStatusUpdateView.as_view()),
]
