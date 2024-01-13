from django.urls import path

from . import views as custom_views


urlpatterns = [
    path('create/', custom_views.CreateOrderFormAPIView.as_view(), name='order-create'),
]
