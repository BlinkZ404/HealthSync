from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Profile, Donation, BloodDonor, Product,
    Manufacturer, CartItem, Order, OrderItem
)


# Profile Admin Configuration
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'mobile_number', 'gender', 'dob', 'profile_picture_thumbnail')
    search_fields = ('user__username', 'user__email', 'mobile_number')
    list_filter = ('gender',)

    def profile_picture_thumbnail(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile_picture.url)
        return "No Image"
    profile_picture_thumbnail.short_description = 'Profile Picture'

    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'


# Donation Admin Configuration
@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'donation_date', 'hospital_name', 'receiver_name', 'receiver_number', 'created_at')
    search_fields = ('user__username', 'hospital_name', 'receiver_name')
    list_filter = ('donation_date',)
    ordering = ('-donation_date',)


# Blood Donor Admin Configuration
@admin.register(BloodDonor)
class BloodDonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_number', 'blood_group', 'division', 'district')
    search_fields = ('name', 'mobile_number', 'blood_group')
    list_filter = ('blood_group', 'division', 'district')


# Product Admin Configuration
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'original_price', 'discount_percentage', 'availability', 'manufacturer')
    list_filter = ('availability', 'manufacturer', 'form')
    search_fields = ('name', 'sku')
    ordering = ('name',)
    list_editable = ('price', 'availability')
    readonly_fields = ('discount_percentage',)

    def discount_percentage(self, obj):
        return f"{obj.discount_percentage()}%"
    discount_percentage.short_description = 'Discount (%)'


# Manufacturer Admin Configuration
@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'address')
    search_fields = ('name', 'phone_number')
    ordering = ('name',)


# CartItem Admin Configuration
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'item_total')
    search_fields = ('user__username', 'product__name')
    list_filter = ('product',)
    readonly_fields = ('item_total',)


# Inline OrderItem Display within Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'item_total')
    can_delete = False


# Order Admin Configuration
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status','total_amount', 'delivery_method', 'payment_method', 'created_at')
    list_filter = ('status','delivery_method', 'payment_method', 'created_at')
    search_fields = ('user__username', 'address', 'phone_number', 'status')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)
    readonly_fields = ('total_amount', 'delivery_fee', 'discount', 'created_at')


# OrderItem Admin Configuration
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'item_total')
    search_fields = ('product__name', 'order__id')
    list_filter = ('product',)
    ordering = ('order',)
