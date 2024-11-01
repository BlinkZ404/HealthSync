from django.contrib import admin
from .models import BloodDonor  # Import your model

# Decorator registers the model with the admin site
@admin.register(BloodDonor)
class BloodDonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_number', 'blood_group', 'division', 'district')
    search_fields = ('name', 'mobile_number', 'blood_group')