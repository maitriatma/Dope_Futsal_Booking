from django.contrib import admin
from .models.customer import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email']


# Register your models here.
admin.site.register(Customer, CustomerAdmin)
