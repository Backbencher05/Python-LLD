from django.contrib import admin
from testapp.models import  User, ShippingAddress

# Register your models here.

admin.site.register(User)
admin.site.register(ShippingAddress)