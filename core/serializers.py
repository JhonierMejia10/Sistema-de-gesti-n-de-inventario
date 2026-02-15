from rest_framework import serializers
from .models import EstadoPago
from django.contrib.auth.models import User

class EstadoPagoSerializer(serializers.ModelSerializer):    
    class Meta:
        model = EstadoPago
        fields = ['nombre','descripcion']
        only_read_fields = ['id']
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password']
        extra_kwargs = {
            'password':{'write_only': True}
        }
