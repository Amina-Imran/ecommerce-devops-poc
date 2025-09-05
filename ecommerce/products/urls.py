from django.urls import path
from . import views

app_name = "products"   

urlpatterns = [
    path("", views.product_list, name="list"),      # use 'products:list'
    path("<int:pk>/", views.product_detail, name="detail"),  # use 'products:detail'
]
