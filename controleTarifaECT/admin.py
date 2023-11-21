from django.contrib import admin

# Register your models here.

from .models import Tarifa, CodigoTarifa

admin.site.register(Tarifa)
admin.site.register(CodigoTarifa)