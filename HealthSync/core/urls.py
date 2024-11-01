from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home page route
    path('', views.home, name='home'),

    # Authentication-related routes
    path('login/', views.login_view, name='login'),  # Login page for users
    path('register/', views.register_view, name='register'),  # Registration page for new users
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),  # Password reset page
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),  # Confirmation of password reset request
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # Password reset confirmation page
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  # Password reset completion page

    # Custom logout route using custom view for logout
    path('logout/', views.custom_logout, name='logout'),  # Custom logout action to log out users

    # Profile and user information routes
    path('profile/', views.user_profile, name='user_profile'),  # User profile page
    path('update_profile/', views.update_profile, name='update_profile'),  # Update profile information
    path('add_address/', views.add_address, name='add_address'),  # Add address to user's profile
    path('add_donation/', views.add_donation, name='add_donation'),  # Add donation record to user's profile

    # Informational and legal pages
    path('about/', views.about, name='about'),  # About page
    path('faq/', views.faq, name='faq'),  # Frequently Asked Questions (FAQ) page
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),  # Privacy policy page
    path('refund-policy/', views.refund_policy, name='refund_policy'),  # Refund policy page
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),  # Terms and conditions page

    # B2B registration route
    path('b2b-registration/', views.b2b_registration, name='b2b_registration'),  # Business-to-business registration

    # Health services and product-related routes
    path('medicine/', views.medicine, name='medicine'),  # Medicine view
    path('medicine/<str:sku>/', views.medicine_page, name='medicine_page'), # Medicine page view
    path('doctors/', views.doctors, name='doctors'),  # Doctors listing page
    path('disease-prediction/', views.disease_prediction, name='disease_prediction'),  # Disease prediction page
    path('blood-donors/', views.donor_view, name='donors'), # Donor list page
    path('add_donor/', views.add_donor, name='add_donor'), # Add donor info to donor list page

    # Shopping and e-commerce routes
    path('cart/', views.cart, name='cart'),  # Shopping cart page
    path('checkout/', views.checkout, name='checkout'),  # Checkout page

    # Test page for development or debugging purposes
    path('test/', views.test, name='test'),  # Test page for functionality verification
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
]

# Add static and media URLs in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom 404 error handler route
handler404 = 'core.views.error_404'  # Custom error handler for 404 page not found