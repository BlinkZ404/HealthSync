from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from . import views

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),  # Main home page

    # User Authentication & Profile Management
    path('request-otp/', views.request_otp_view, name='request_otp'),  # Request an OTP for login/registration
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),  # Verify the OTP entered by the user
    path('logout/', views.custom_logout, name='logout'),  # Log out the user
    path('profile/', views.user_profile, name='user_profile'),  # User profile page
    path('update_profile/', views.update_profile, name='update_profile'),  # Update user profile details
    path('add_donation/', views.add_donation, name='add_donation'),  # Add a donation record
    path('delete-donation/<int:donation_id>/', views.delete_donation, name='delete_donation'),  # Delete a donation record

    # Informational and Legal Pages
    path('about/', views.about, name='about'),  # About us page
    path('faq/', views.faq, name='faq'),  # Frequently Asked Questions page
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),  # Privacy policy
    path('refund-policy/', views.refund_policy, name='refund_policy'),  # Refund policy
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),  # Terms and conditions
    path('pharmacy-registration/', views.pharmacy_registration_view, name='pharmacy_registration'),  # Pharmacy registration page
    path('b2b-registration/', views.b2b_registration, name='b2b_registration'),  # B2B registration page

    # Health Services and Product Management
    path('medicine/', views.medicine, name='medicine'),  # List of medicines
    path('medicine/<str:sku>/', views.medicine_page, name='medicine_page'),  # Medicine detail view by SKU
    path('doctors/', views.doctors, name='doctors'),  # List of doctors
    path('disease-prediction/', views.disease_prediction, name='disease_prediction'),  # Disease prediction tool
    path('blood-donors/', views.donor_view, name='donors'),  # List of blood donors
    path('add_donor/', views.add_donor, name='add_donor'),  # Add a new blood donor

    # Appointment Management
    path('book_appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),  # Book an appointment
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),  # Cancel an appointment
    path('edit_appointment/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),  # Edit an appointment
    path('get_available_slots/<int:doctor_id>/', views.get_available_slots, name='get_available_slots'),  # Fetch available slots

    # Shopping and E-commerce
    path('cart/', views.view_cart, name='view_cart'),  # View items in the shopping cart
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add a product to the cart
    path('update-cart-item/<int:item_id>/', views.update_cart_item_quantity, name='update_cart_item_quantity'),  # Update cart item quantity
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove an item from the cart
    path('apply_discount_code/', views.apply_discount_code, name='apply_discount_code'),  # Apply a discount code
    path('apply_gift_voucher/', views.apply_gift_voucher, name='apply_gift_voucher'),  # Apply a gift voucher
    path('checkout/', views.checkout, name='checkout'),  # Checkout process
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),  # Order confirmation page

    # Product Search
    path('search-products/', views.search_products, name='search_products'),  # AJAX-based product search

]

# Static and Media Routes (for development)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom Error Handlers
handler404 = 'core.views.error_404'
