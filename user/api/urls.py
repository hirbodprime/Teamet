from django.urls import path

from . import views as custom_views


urlpatterns = [
    path('signup/', custom_views.SignupAPIView.as_view(), name='signup'),
]
