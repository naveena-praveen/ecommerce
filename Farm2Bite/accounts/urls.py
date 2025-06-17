from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.email_login, name='login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('logout/', views.logout_view, name='logout'),
]
