from django.urls import path
from .views import CarritoListCreateAPIView

urlpatterns = [
    path('carrito', CarritoListCreateAPIView.as_view())
]