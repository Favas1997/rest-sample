from RESTapi.models import product
from django.urls import path
from RESTapi import views

urlpatterns = [
     path("api/",views.api_overview,name="api"),
     path("api/product/",views.ProductList.as_view()),
     path("api/create/",views.ProductCreate.as_view()),
     path("api/action/<int:id>/",views.ProductRetrieveUpdateDestroyAPIView.as_view()),
]