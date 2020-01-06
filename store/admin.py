from django.contrib import admin
from .models import Order
from .models import Client
from .models import ProductDiscount
from .models import Product
from .models import Discount

admin.site.register(Order)
admin.site.register(Client)
admin.site.register(ProductDiscount)
admin.site.register(Product)
admin.site.register(Discount)