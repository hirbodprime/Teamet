from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from . import serializers as custom_serializers


class CreateOrderFormAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializers.CreateOrderFormSerializer
    