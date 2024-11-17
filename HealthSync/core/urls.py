from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from . import views


urlpatterns = [
    # Home Page
    path('', views.home, name='home'),  # Main home page

    # Authentication-related routes
    path('request-otp/', views.request_otp_view, name='request_otp'), # Route for requesting an OTP, triggers OTP generation and email
    path('verify-otp/', views.verify_otp_view, name='verify_otp'), # Route for verifying the OTP entered by the user

    # Custom logout route
    path('logout/', views.custom_logout, name='logout'),  # Custom logout action to log out users

    # Profile and user information routes
    path('profile/', views.user_profile, name='user_profile'),  # User profile page
    path('update_profile/', views.update_profile, name='update_profile'),  # Update profile information
    path('add_donation/', views.add_donation, name='add_donation'),  # Add donation record to user's profile
    path('delete-donation/<int:donation_id>/', views.delete_donation, name='delete_donation'), # Delete donation record from user's profile

    # Informational and legal pages
    path('about/', views.about, name='about'),  # About page
    path('faq/', views.faq, name='faq'),  # Frequently Asked Questions (FAQ) page
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),  # Privacy policy page
    path('refund-policy/', views.refund_policy, name='refund_policy'),  # Refund policy page
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),  # Terms and conditions page
    path('pharmacy-registration/', views.pharmacy_registration_view, name='pharmacy_registration'),  # Pharmacy registration page

    # B2B registration route
    path('b2b-registration/', views.b2b_registration, name='b2b_registration'),  # Business-to-business registration

    # Health services and product-related routes
    path('medicine/', views.medicine, name='medicine'),  # Medicine listing view
    path('medicine/<str:sku>/', views.medicine_page, name='medicine_page'),  # Individual medicine detail view
    path('doctors/', views.doctors, name='doctors'),  # Doctors listing page
    path('disease-prediction/', views.disease_prediction, name='disease_prediction'),  # Disease prediction page
    path('blood-donors/', views.donor_view, name='donors'),  # Blood donor list page
    path('add_donor/', views.add_donor, name='add_donor'),  # Add donor info to donor list page

    #appointment urls
    path('book_appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('edit_appointment/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('get_available_slots/<int:doctor_id>/', views.get_available_slots, name='get_available_slots'),

    # Shopping and e-commerce routes
    path('cart/', views.view_cart, name='view_cart'),  # View cart page
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add product to cart
    path('update-cart-item/<int:item_id>/', views.update_cart_item_quantity, name='update_cart_item_quantity'),  # Update cart item quantity
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove item from cart
    path('apply_discount_code/', views.apply_discount_code, name='apply_discount_code'),  # Apply a discount code to the cart
    path('apply_gift_voucher/', views.apply_gift_voucher, name='apply_gift_voucher'),  # Apply a gift voucher to the cart
    path('checkout/', views.checkout, name='checkout'),  # Checkout page
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),  # Order confirmation page

    # Product search and miscellaneous routes
    path('test/', views.test, name='test'),  # Test page for development or debugging purposes
    path('search-products/', views.search_products, name='search_products'),  # AJAX product search results
]

# Add static and media URLs in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom 404 error handler route
handler404 = 'core.views.error_404'


