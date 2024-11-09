from django.contrib import admin
from .models import *

admin.site.register(Cart)
admin.site.register(Cart_Item)
admin.site.register(Order)
admin.site.register(Order_Item)

