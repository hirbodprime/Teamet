from django.contrib import admin

from .models import OrderFormModel


@admin.register(OrderFormModel)
class OrderAdmin(admin.ModelAdmin):
    fields = ['created_at', 'first_name', 'last_name', 'email', 'phone', 'company', 'products']
    readonly_fields = ['created_at']
