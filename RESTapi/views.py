from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import ProductSerializer
from .models import product

@api_view(['GET'])
def api_overview(request):
    api_urls={
        'productlist':'/product/',
        'addproduct':'/create/',
        'action':'/action/<int:id>/'

    }
    return Response(api_urls)

class ProductList(ListAPIView):
    queryset=product.objects.all()
    serializer_class = ProductSerializer
    filter_backends=(DjangoFilterBackend,SearchFilter)
    filter_fields= ('id','name',)
    search_fields=('id','name')
class ProductCreate(CreateAPIView):
    serializer_class=ProductSerializer

    def create(self,request,*args,**kwargs):
        try:
            price=request.data.get('price')
            if price is not None and float(price)<= 0.0:
                raise ValidationError({'price':'Must be above $0.00'})
        except ValueError:
            raise ValidationError({'price':'a valid number is required'})

        return super().create(request,*args,**kwargs)
class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset=product.objects.all()
    lookup_field= 'id'
    serializer_class=ProductSerializer

    def delete(self,request,*args,**kwargs):
        product_id=request.data.get('id')
        response=super().delete(request,*args,**kwargs)
        if response.status_code==204:
            cache.delete('product_data_{}'.format(product_id))
        return response
    def update(self,request,*args,**kwargs):
        response=super().update(request,*args,**kwargs)
        if response.status_code==200:
            product=response.data
            cache.set('product_data_{}'.format(product['id']),{
                'name':product['name'],
                'description':product['description'],
                'price':product['price'],
            })
        return response


