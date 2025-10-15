from rest_framework import serializers
from .models import MovimientoInventario
from django.contrib.auth.models import User

class MovimientoSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovimientoInventario
        fields = '__all__'
        read_only_fields = ['id','usuario'] 

        

    
    