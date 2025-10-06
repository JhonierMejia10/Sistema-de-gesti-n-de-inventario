from django.urls import path
from .views import vistaprueba

urlpatterns = [
    path('prueba', vistaprueba, )
]

