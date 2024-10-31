from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('refund-policy/', views.refund_policy, name='refund_policy'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    path('b2b-registration/', views.b2b_registration, name='b2b_registration'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('medicine/', views.medicine, name='medicine'),
    path('doctors/', views.doctors, name='doctors'),
    path('blood-donation/', views.donation, name='blood_donation'),
    path('disease-prediction/', views.disease_prediction, name='disease_prediction'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('test/', views.test, name='test'),
    path('logout/', LogoutView.as_view(), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'core.views.error_404'