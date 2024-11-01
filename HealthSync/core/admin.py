from django.contrib import admin
from .models import BloodDonor, Product, Manufacturer  # Import your model

# Decorator registers the model with the admin site
@admin.register(BloodDonor)
class BloodDonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_number', 'blood_group', 'division', 'district')
    search_fields = ('name', 'mobile_number', 'blood_group')

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'price', 'availability', 'manufacturer']
    list_filter = ['availability', 'manufacturer']
    search_fields = ['name', 'sku']

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone_number']
    search_fields = ['name']  #


admin.site.register(Product, ProductAdmin)
admin.site.register(Manufacturer)