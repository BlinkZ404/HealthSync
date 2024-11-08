from django.contrib import admin
from .models import BloodDonor, Doctor ,  AvailableDate, AvailableTime ,Appointment # Import your model

# Decorator registers the model with the admin site
@admin.register(BloodDonor)
class BloodDonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_number', 'blood_group', 'division', 'district')
    search_fields = ('name', 'mobile_number', 'blood_group')


# admin.site.register(Doctor)
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'hospital')
    filter_horizontal = ('available_dates', 'available_times')

admin.site.register(AvailableDate)
admin.site.register(AvailableTime)
admin.site.register(Appointment)