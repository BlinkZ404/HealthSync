from django.db import models
from django.contrib.auth.models import User

# Profile model to extend the User model with additional attributes
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # New field for profile picture

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Address model to store user's address details
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15)
    road = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.road}"

# Donation model to track user donation details
class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    donation_date = models.DateField()
    hospital_name = models.CharField(max_length=255)
    receiver_name = models.CharField(max_length=255)
    receiver_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation by {self.user.username} on {self.donation_date}"
