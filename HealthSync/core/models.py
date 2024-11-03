from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta


# Profile model to extend the User model with additional attributes
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


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


# Donor model to save donor details
class BloodDonor(models.Model):
    name = models.CharField(max_length=100, default='Anonymous')
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    blood_group = models.CharField(max_length=5)
    division = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.blood_group} ({self.mobile_number})"

# Manufacturer model to save manufacturer details
class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

# Product model to save product details
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

# CartItem model to save cart items
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def item_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

# Order model to save order details
class Order(models.Model):
    DELIVERY_METHOD_CHOICES = [
        ('Home Delivery', 'Home Delivery (1-2 Days)'),
        ('Express Delivery', 'Express Delivery (1-2 Hours)'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('Online Payment', 'Online Payment (bKash, Nagad, Credit/Debit Card)'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
        ('Refunded', 'Refunded'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_METHOD_CHOICES, default='Home Delivery')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='COD')
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

# OrderItem model to save order item details
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x{self.quantity} in Order #{self.order.id}"


# Pharmacy model to save registered pharmacies
class PharmacyRegistration(models.Model):
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    pharmacy_name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=50)
    license_upload = models.FileField(upload_to='license_uploads/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pharmacy_name} - {self.full_name}"


class OTP(models.Model):
    email = models.EmailField()  # Add this line to store the email address
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=5)