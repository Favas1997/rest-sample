from django.db.models.base import Model
from rest_framework import serializers
from . models import product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=product
        # fields=('id','name','description','price','sale_start','sale_end')
        fields='__all__'
