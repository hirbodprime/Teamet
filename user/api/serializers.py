from django.conf import settings
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from user.models import CustomUser


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True},}

    def validate_password(self, value):
        # using CustomeUserModel to hash the password
        user = CustomUser()

        try:
            validate_password(value)
            user.set_password(value)

        except Exception as e:
            raise serializers.ValidationError(str(e))
        
        return user.password