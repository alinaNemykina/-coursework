from django.contrib import admin
from .models import *

admin.site.register(Order)
admin.site.register(Client)
admin.site.register(ProductDiscount)
admin.site.register(Product)
admin.site.register(Discount)