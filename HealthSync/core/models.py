from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Profile model to extend the User model with additional attributes
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

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
    name = models.CharField(max_length=100, default='Anonymous')
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    blood_group = models.CharField(max_length=5)
    division = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.blood_group} ({self.mobile_number})"

class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    IN_STOCK = 'In Stock'
    OUT_OF_STOCK = 'Out of Stock'
    AVAILABILITY_CHOICES = [
        (IN_STOCK, 'In Stock'),
        (OUT_OF_STOCK, 'Out of Stock'),
    ]

    TABLET = 'Tablet'
    SYRUP = 'Syrup'
    INJECTION = 'Injection'
    FORM_CHOICES = [
        (TABLET, 'Tablet'),
        (SYRUP, 'Syrup'),
        (INJECTION, 'Injection'),
    ]

    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True,  validators=[MinValueValidator(0)])
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                         validators=[MinValueValidator(0)])
    short_description = models.TextField()
    form = models.CharField(max_length=50, choices=FORM_CHOICES ,db_index=True)
    pack_size = models.CharField(max_length=50)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, db_index=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, db_index=True)
    description = models.TextField()
    directions = models.TextField()
    warnings = models.TextField()
    image = models.ImageField(upload_to='product_images/')

    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            discount = ((self.original_price - self.price) / self.original_price) * 100
            return round(discount, 2)
        return 0

    def __str__(self):
        return self.name


