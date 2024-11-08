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


# Donormodel to save donor details
class BloodDonor(models.Model):
    name = models.CharField(max_length=100, default='Anonymous')  # Name cannot be null
    mobile_number = models.CharField(max_length=15, blank=True, null=True)  # Allow nulls
    blood_group = models.CharField(max_length=5)
    division = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.blood_group} ({self.mobile_number})"

#doctors model

class Doctor(models.Model):
    DIVISION_CHOICES = [
        ('Barishal', 'Barishal'),
        ('Chattogram', 'Chattogram'),
        ('Dhaka', 'Dhaka'),
        ('Khulna', 'Khulna'),
        ('Mymensingh', 'Mymensingh'),
        ('Rajshahi', 'Rajshahi'),
        ('Rangpur', 'Rangpur'),
        ('Sylhet', 'Sylhet'),
    ]

    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    experience = models.IntegerField(null=True)
    hospital = models.CharField(max_length=100)
    address = models.TextField()
    photo = models.ImageField(upload_to='doctors/', default='doctors/default.jpg')
    expertise = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], default='Male')
    division = models.CharField(max_length=20, choices=DIVISION_CHOICES, default='Dhaka')  # New field for division

    # New fields for appointment scheduling (Sa)
    available_dates = models.ManyToManyField('AvailableDate', blank=True)
    available_times = models.ManyToManyField('AvailableTime', blank=True)

    def __str__(self):
        return self.name


# Appointment model
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments',  default=1)
    patient_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    # blood_group = models.CharField(max_length=3, blank=True)
    # disease_description = models.TextField(blank=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    # New field for tracking appointment status
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return f"  {self.patient_name} - {self.phone_number} -  {self.doctor.name} on  {self.appointment_date} at {self.appointment_time} "

class AvailableDate(models.Model):
    date = models.DateField()
    def __str__(self):
        return self.date.strftime("%Y-%m-%d")

class AvailableTime(models.Model):
    time = models.TimeField()

    def __str__(self):
        return self.time.strftime("%H:%M")