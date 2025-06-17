from django.urls import path
from . import views
urlpatterns = [
    path('', views.cart_details, name='cart'),
    path('add/<int:product_id>/', views.add_cart, name='addcart'),
    path('dec/<int:product_id>/',views.mincart,name='mincart'),
    path('inc/<int:product_id>/',views.inccart,name='inccart'),
    path('remove/<int:product_id>/',views.deleteitem,name='deleteitem'),
]

