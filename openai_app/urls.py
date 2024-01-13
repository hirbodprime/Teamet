from django.urls import path,include

urlpatterns = [
    path('api/',include('openai_app.api.urls')),
]
