from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from decimal import Decimal
import random
from django.core.mail import send_mail
import json

from .models import (
    Profile, Donation, BloodDonor, Product, Manufacturer,
    CartItem, Order, OrderItem, PharmacyRegistration, OTP, Doctor , AvailableDate, AvailableTime , Appointment
)

# Render the home page
def home(request):
    return render(request, 'home.html')


# Handle OTP request for registration/login
def request_otp_view(request):
    if request.method == 'POST':
        # Handle AJAX request for resending OTP
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = json.loads(request.body)
            email = data.get('email')

            if email:
                # Delete existing OTPs and create a new one
                OTP.objects.filter(email=email).delete()
                otp_code = random.randint(100000, 999999)
                OTP.objects.create(email=email, code=str(otp_code))

                # Send OTP email
                try:
                    send_mail(
                        'Your HealthSync Login OTP',
                        f'Your OTP is: {otp_code}',
                        'noreply@healthsync.com',
                        [email],
                        fail_silently=False,
                    )
                    messages.success(request, 'A new OTP has been sent to your email.')
                    return JsonResponse({'success': True})
                except Exception:
                    messages.error(request, 'There was an error sending the OTP. Please try again later.')
                    return JsonResponse({'success': False})
            else:
                messages.error(request, 'Please provide a valid email address.')
                return JsonResponse({'success': False})

        # Non-AJAX POST request handling for initial OTP request
        email = request.POST.get('email')
        if email:
            OTP.objects.filter(email=email).delete()
            otp_code = random.randint(100000, 999999)
            OTP.objects.create(email=email, code=str(otp_code))

            try:
                send_mail(
                    'Your HealthSync Login OTP',
                    f'Your OTP is: {otp_code}',
                    'noreply@healthsync.com',
                    [email],
                    fail_silently=False,
                )
                request.session['email'] = email
                messages.success(request, 'Your OTP has been sent to your email.')
                return HttpResponseRedirect('/verify-otp/')
            except Exception:
                messages.error(request, 'Failed to send OTP. Please try again later.')
                return render(request, 'request_otp.html')

        messages.error(request, 'Please enter a valid email address.')
        return render(request, 'request_otp.html')

    return render(request, 'request_otp.html')


# Handle OTP verification
def verify_otp_view(request):
    if request.method == 'POST':
        email = request.session.get('email')
        input_otp = request.POST.get('otp')

        try:
            otp_instance = OTP.objects.filter(email=email, code=input_otp).latest('created_at')

            # Validate OTP and log in user
            if otp_instance and otp_instance.is_valid():
                user, created = User.objects.get_or_create(username=email, email=email)
                login(request, user)

                otp_instance.delete()
                del request.session['email']
                return redirect('home')
            else:
                messages.error(request, "Invalid or expired OTP.")
        except OTP.DoesNotExist:
            messages.error(request, "Invalid email or OTP.")

        return render(request, 'verify_otp.html')

    return render(request, 'verify_otp.html')


# Display user profile
@login_required(login_url='request_otp')
def user_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    donations = Donation.objects.filter(user=request.user).order_by('-donation_date')
    appointments = request.user.appointments.all()

    context = {
        'user': request.user,
        'profile': profile,
        'orders': orders,
        'donations': donations,
        'appointments': appointments,
    }
    return render(request, 'user_profile.html', context)


# Update user profile information
@login_required(login_url='request_otp')
def update_profile(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        mobile_number = request.POST.get('mobile_number')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        profile_picture = request.FILES.get('profile_picture')

        try:
            # Update user model fields
            user = request.user
            user.email = email
            user.first_name = full_name.split(" ")[0] if full_name else ""
            user.last_name = " ".join(full_name.split(" ")[1:]) if full_name else ""
            user.save()

            # Update profile model fields
            profile, created = Profile.objects.get_or_create(user=user)
            profile.mobile_number = mobile_number
            profile.gender = gender
            if dob:
                profile.dob = dob
            if profile_picture:
                profile.profile_picture = profile_picture
            profile.save()

            messages.success(request, "Profile updated successfully.")
        except Exception as e:
            messages.error(request, f"Error updating profile: {e}")

        return redirect('user_profile')

    return redirect('user_profile')


# Add a donation entry
@login_required
def add_donation(request):
    if request.method == 'POST':
        donation_date = request.POST.get('donation_date')
        hospital_name = request.POST.get('hospital_name')
        receiver_name = request.POST.get('receiver_name')
        receiver_number = request.POST.get('receiver_number')

        Donation.objects.create(
            user=request.user,
            donation_date=donation_date,
            hospital_name=hospital_name,
            receiver_name=receiver_name,
            receiver_number=receiver_number
        )

        messages.success(request, "Donation history added successfully.")
        return redirect('user_profile')

    return redirect('user_profile')


# Delete a donation entry
@login_required
def delete_donation(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id, user=request.user)
    donation.delete()
    messages.success(request, "Donation record deleted successfully.")
    return redirect('user_profile')


# Logout the user
def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('request_otp')


# Register a new blood donor
def add_donor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile_number = request.POST.get('mobile_number')
        blood_group = request.POST.get('blood_group')
        division = request.POST.get('division')
        district = request.POST.get('district')

        BloodDonor.objects.create(
            name=name,
            mobile_number=mobile_number,
            blood_group=blood_group,
            division=division,
            district=district
        )
        messages.success(request, "Donor registered successfully!")
        return redirect('donors')

    return redirect('donors')


# View all registered donors
def donor_view(request):
    donors = BloodDonor.objects.all()
    return render(request, 'donation.html', {'donors': donors})


# Static pages
def about(request): return render(request, 'about.html')
def faq(request): return render(request, 'faq.html')
def privacy_policy(request): return render(request, 'privacy.html')
def refund_policy(request): return render(request, 'refund_policy.html')
def terms_conditions(request): return render(request, 'terms.html')
def b2b_registration(request): return render(request, 'b2b_registration.html')
def medicine(request): return render(request, 'medicine.html')
def doctors(request): return render(request, 'doctors.html')
def disease_prediction(request): return render(request, 'disease_prediction.html')
def appointment(request): return render(request, 'doctors.html')
def cart(request): return render(request, 'cart.html')
def checkout(request): return render(request, 'checkout.html')
def error_404(request, exception): return render(request, '404.html', status=404)
def test(request): return render(request, 'test.html')


# View for displaying a single product's details
def medicine_page(request, sku):
    product = get_object_or_404(Product, sku=sku)
    return render(request, 'medicine_page.html', {'product': product})


# Filter and sort products
def medicine(request):
    products = Product.objects.all()
    sort_order = request.GET.get('sort')
    if sort_order == 'asc':
        products = products.order_by('price')
    elif sort_order == 'desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('id')

    availability = request.GET.getlist('availability')
    if availability:
        products = products.filter(availability__in=availability)

    manufacturer = request.GET.getlist('manufacturer')
    if manufacturer:
        products = products.filter(manufacturer__name__in=manufacturer)

    form = request.GET.getlist('form')
    if form:
        products = products.filter(form__in=form)

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'availability_options': [choice[0] for choice in Product.AVAILABILITY_CHOICES],
        'form_options': [choice[0] for choice in Product.FORM_CHOICES],
        'manufacturers': Manufacturer.objects.all(),
        'selected_availability': availability,
        'selected_form': form,
        'selected_manufacturer': manufacturer,
        'sort_order': sort_order,
    }
    return render(request, 'medicine.html', context)


# Apply discount code to cart
def apply_discount_code(request):
    if request.method == 'POST':
        discount_code = request.POST.get('discount_code', '')
        return redirect('view_cart')
    return HttpResponseRedirect('/')


# Apply gift voucher to cart
def apply_gift_voucher(request):
    if request.method == 'POST':
        gift_voucher = request.POST.get('gift_voucher', '')
        return redirect('view_cart')
    return HttpResponseRedirect('/')


# Add item to cart
@login_required(login_url='request_otp')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    messages.success(request, f"{product.name} added to cart.")
    return redirect('view_cart')


# View all items in cart
@login_required(login_url='request_otp')
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = sum(item.item_total() for item in cart_items)
    total = subtotal

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': total,
    }
    return render(request, 'cart.html', context)


# Update item quantity in cart
@login_required(login_url='request_otp')
def update_cart_item_quantity(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, "Quantity updated.")
        else:
            messages.error(request, "Invalid quantity.")
    return redirect('view_cart')


# Remove item from cart
@login_required(login_url='request_otp')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('view_cart')


# Handle checkout process
@login_required(login_url='request_otp')
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Please add items to proceed to checkout.")
        return redirect('view_cart')

    if request.method == 'POST':
        full_name = request.POST.get("full_name")
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        delivery_method = request.POST.get('delivery_method')
        payment_method = request.POST.get('payment_method')

        subtotal = sum(item.item_total() for item in cart_items)
        delivery_fee = Decimal('100.00') if delivery_method == 'Express Delivery' else Decimal('50.00')
        discount = Decimal('0.00')
        total_amount = subtotal + delivery_fee - discount

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            phone_number=phone_number,
            delivery_method=delivery_method,
            payment_method=payment_method,
            delivery_fee=delivery_fee,
            discount=discount,
            total_amount=total_amount,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                item_total=item.item_total(),
            )
            item.delete()

        messages.success(request, "Order placed successfully!")
        return redirect('order_confirmation', order_id=order.id)

    context = {
        'cart_items': cart_items,
        'subtotal': sum(item.item_total() for item in cart_items),
        'delivery_fee': 50,
        'discount': 0,
        'total': sum(item.item_total() for item in cart_items) + 50 - 0,
    }
    return render(request, 'checkout.html', context)


# Display order confirmation
@login_required(login_url='request_otp')
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.user != request.user:
        messages.error(request, "You do not have permission to view this order.")
        return redirect('home')

    return render(request, 'order_confirmation.html', {'order': order})


# Handle pharmacy registration
def pharmacy_registration_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        mobile_number = request.POST.get('mobile_number')
        pharmacy_name = request.POST.get('pharmacy_name')
        license_number = request.POST.get('license_number')
        license_upload = request.FILES.get('license_upload')

        if license_upload:
            if license_upload.size > 50 * 1024 * 1024:
                messages.error(request, 'File size exceeds 50 MB. Please upload a smaller file.')
                return redirect('pharmacy_registration')
            if not license_upload.name.endswith(('.pdf', '.jpg', '.jpeg')):
                messages.error(request, 'Unsupported file format. Please upload a PDF, JPG, or JPEG file.')
                return redirect('pharmacy_registration')

        PharmacyRegistration.objects.create(
            full_name=full_name,
            mobile_number=mobile_number,
            pharmacy_name=pharmacy_name,
            license_number=license_number,
            license_upload=license_upload
        )

        messages.success(request, 'Your information has been received. We will contact you soon.')
        return redirect('pharmacy_registration')

    return render(request, 'b2b_registration.html')


# Search for products based on user query
def search_products(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query)[:5]

    results = [
        {
            'name': product.name,
            'sku': product.sku,
            'price': str(product.price),
            'image': product.image.url if product.image else '',
        }
        for product in products
    ]

    return JsonResponse(results, safe=False)


# doctors views

def doctors(request):
    # Get filter parameters from the request
    gender = request.GET.get('gender')
    specialty = request.GET.get('specialty')
    division = request.GET.get('division')
    selected_date = request.GET.get('date')

    # Filter queryset based on parameters
    doctors = Doctor.objects.all()
    if gender:
        doctors = doctors.filter(gender=gender)
    if specialty:
        doctors = doctors.filter(specialty=specialty)
    if division:
        doctors = doctors.filter(division=division)

    if selected_date:
        available_date = AvailableDate.objects.filter(date=selected_date).first()
        if available_date:
            doctors = doctors.filter(available_dates=available_date)
        else:
            doctors = Doctor.objects.none()

    return render(request, 'doctors.html', {
        'doctors': doctors,
        'specialties': dict(Doctor.SPECIALTY_CHOICES).values(),
    })


# Booking Appointment
def book_appointment(request, doctor_id):
    if request.method == "POST":
        # Retrieve form data directly from POST request
        doctor = get_object_or_404(Doctor, id=doctor_id)
        patient_name = request.POST.get('patient_name')
        phone_number = request.POST.get('phone_number')
        # blood_group = request.POST.get('blood_group')
        # disease_description = request.POST.get('disease_description')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')

        # Save the appointment in the database
        appointment = Appointment.objects.create(
            doctor=doctor,
            patient_name=patient_name,
            phone_number=phone_number,
            # blood_group=blood_group,
            # disease_description=disease_description,

            appointment_date=appointment_date,
            appointment_time=appointment_time,
        )

        messages.success(request, "Appointment booked successfully.")
        return redirect('user_profile')  # Redirect to user's appointments section

    return redirect('doctors')