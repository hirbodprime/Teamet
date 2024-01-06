from django.contrib.auth import get_user_model
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


User = get_user_model()


class OrderFormModel(models.Model):
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    phone = PhoneNumberField()
    company = models.CharField(max_length=256)
    products = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}-{self.user.email}: {self.products}'
    