from django.contrib import admin

from mainapp.models import DeviceAuth, DeviceFetch, Transaction

# Register your models here.
admin.site.register(DeviceFetch)
admin.site.register(Transaction)
admin.site.register(DeviceAuth)