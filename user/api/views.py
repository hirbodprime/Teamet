from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from .serializers import SignUpSerializer


class SignupAPIView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
