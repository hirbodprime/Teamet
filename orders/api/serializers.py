from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField

from orders.models import OrderFormModel


class CreateOrderFormSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField()

    class Meta:
        model = OrderFormModel
        fields = ['user', 'first_name', 'last_name', 'phone', 'email', 'company', 'products']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
