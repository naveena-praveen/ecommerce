from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('search',views.search,name='search'),
    path('product/<slug:c_slug>/<slug:product_slug>/',views.product_detail,name='details'),
    path('category/<slug:c_slug>/', views.Category_lists, name='category_list'),
   
]