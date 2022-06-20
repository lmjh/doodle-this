from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("webhook/", webhook, name="webhook"),
    path(
        "order_confirmed/<order_number>",
        views.order_confirmed,
        name="order_confirmed",
    ),
]
