from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def vistaprueba(request):
    return JsonResponse({'message': "Vista de usuario funcionando correctamente"})
