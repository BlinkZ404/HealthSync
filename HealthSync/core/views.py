from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def about(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'faq.html')

def privacy_policy(request):
    return render(request, 'privacy.html')

def refund_policy(request):
    return render(request, 'refund_policy.html')

def terms_conditions(request):
    return render(request, 'terms.html')

def b2b_registration(request):
    return render(request, 'b2b_registration.html')

def user_profile(request):
    return render(request, 'user_profile.html')

def medicine(request):
    return render(request, 'medicine.html')

def doctors(request):
    return render(request, 'doctors.html')

def donation(request):
    return render(request, 'donation.html')

def disease_prediction(request):
    return render(request, 'disease_prediction.html')

def appointment(request):
    return render(request, 'doctors.html')

def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')

def error_404(request, exception):
    return render(request, '404.html', status=404)

def test(request):
    return render(request, 'test.html')
