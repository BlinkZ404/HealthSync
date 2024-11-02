from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Donation
from django.contrib.auth import logout
from .models import BloodDonor, Product, Manufacturer, CartItem, Order, OrderItem, PharmacyRegistration
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from decimal import Decimal
from django.db import transaction

def home(request):
    # Render the home page
    return render(request, 'home.html')

# Handle user registration
def register_view(request):
    # Redirect authenticated users to home page
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validate password criteria
        if len(password) < 8 or not any(c.islower() for c in password) or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
            messages.error(request, "Password must be at least 8 characters and include uppercase, lowercase, and a digit.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
        else:
            # Create a new user and log them in
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('home')

    return render(request, 'register.html')


# Handle user login
def login_view(request):
    # Redirect authenticated users to home page
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Use email to retrieve username
        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return render(request, 'login.html')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'login.html')

@login_required
def user_profile(request):
    # Get or create the profile associated with the user
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Fetch all orders for the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # Pass user, profile, and order data to the template
    context = {
        'user': request.user,
        'profile': profile,
        'orders': orders
    }

    return render(request, 'user_profile.html', context)

# Handle profile updates
@login_required
def update_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        mobile_number = request.POST.get('mobile_number')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        profile_picture = request.FILES.get('profile_picture')

        try:
            # Update User model fields
            user = request.user
            user.username = username
            user.email = email
            user.first_name = full_name.split(" ")[0] if full_name else ""
            user.last_name = " ".join(full_name.split(" ")[1:]) if full_name else ""
            user.save()

            # Update Profile model fields if applicable
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



# Add a donation entry for the authenticated user
def add_donation(request):
    if request.method == 'POST':
        donation_date = request.POST.get('donation_date')
        hospital_name = request.POST.get('hospital_name')
        receiver_name = request.POST.get('receiver_name')
        receiver_number = request.POST.get('receiver_number')

        # Save the donation data
        Donation.objects.create(
            user=request.user,
            donation_date=donation_date,
            hospital_name=hospital_name,
            receiver_name=receiver_name,
            receiver_number=receiver_number
        )

        messages.success(request, "Donation history added successfully.")
        return redirect('user_profile')  # Redirect back to profile page

    return redirect('user_profile')

# Logout the user and redirect to the login page
def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


# Add a donor info on donation page
def add_donor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile_number = request.POST.get('mobile_number')
        blood_group = request.POST.get('blood_group')
        division = request.POST.get('division')
        district = request.POST.get('district')

        # Save the donor information
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

# Render the Donation page
def donor_view(request):
    donors = BloodDonor.objects.all()
    return render(request, 'donation.html', {'donors': donors})


# Render the About Us page
def about(request):
    return render(request, 'about.html')

# Render the FAQ page
def faq(request):
    return render(request, 'faq.html')

# Render the Privacy Policy page
def privacy_policy(request):
    return render(request, 'privacy.html')

# Render the Refund Policy page
def refund_policy(request):
    return render(request, 'refund_policy.html')

# Render the Terms and Conditions page
def terms_conditions(request):
    return render(request, 'terms.html')

# Render the B2B Registration page
def b2b_registration(request):
    return render(request, 'b2b_registration.html')

# Render the Medicine page
def medicine(request):
    return render(request, 'medicine.html')

def medicine_page(request):
    return render(request, 'medicine_page.html')

# Render the Doctors page
def doctors(request):
    return render(request, 'doctors.html')

# Render the Donation page

# Render the Disease Prediction page
def disease_prediction(request):
    return render(request, 'disease_prediction.html')

# Render the Appointment page
def appointment(request):
    return render(request, 'doctors.html')

# Render the Cart page
def cart(request):
    return render(request, 'cart.html')

# Render the Checkout page
def checkout(request):
    return render(request, 'checkout.html')

# Render a custom 404 error page
def error_404(request, exception):
    return render(request, '404.html', status=404)

# Render the Test page
def test(request):
    return render(request, 'test.html')


def medicine_page(request, sku):
    product = get_object_or_404(Product, sku=sku)
    return render(request, 'medicine_page.html', {'product': product})

def medicine(request):
    products = Product.objects.all()

    # Apply sorting
    sort_order = request.GET.get('sort')
    if sort_order == 'asc':
        products = products.order_by('price')
    elif sort_order == 'desc':
        products = products.order_by('-price')

    # Apply filtering based on request parameters
    availability = request.GET.getlist('availability')
    if availability:
        products = products.filter(availability__in=availability)

    manufacturer = request.GET.getlist('manufacturer')
    if manufacturer:
        products = products.filter(manufacturer__name__in=manufacturer)

    form = request.GET.getlist('form')
    if form:
        products = products.filter(form__in=form)

    # Paginate the filtered and sorted queryset
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



def apply_discount_code(request):
    if request.method == 'POST':
        discount_code = request.POST.get('discount_code', '')
        return redirect('view_cart')
    return HttpResponseRedirect('/')



def apply_gift_voucher(request):
    if request.method == 'POST':
        gift_voucher = request.POST.get('gift_voucher', '')
        return redirect('view_cart')
    return HttpResponseRedirect('/')




@login_required
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



@login_required(login_url='login')
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = sum(item.item_total() for item in cart_items)
    total = subtotal  # Adjust with any additional fees if applicable

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': total,
    }
    return render(request, 'cart.html', context)



@login_required
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



@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('view_cart')



@login_required(login_url='login')
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Please add items to proceed to checkout.")
        return redirect('view_cart')  # Redirect to the cart page

    if request.method == 'POST':
        full_name = request.POST.get("full_name")
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        delivery_method = request.POST.get('delivery_method')
        payment_method = request.POST.get('payment_method')

        subtotal = sum(item.item_total() for item in cart_items)
        if delivery_method == 'Express Delivery':
            delivery_fee = Decimal('100.00')
        else:
            delivery_fee = Decimal('50.00')
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


@login_required(login_url='login')  # Ensures the user is logged in
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Check if the order belongs to the current logged-in user
    if order.user != request.user:
        messages.error(request, "You do not have permission to view this order.")
        return redirect('home')  # Redirect to a suitable page, such as home

    # If the user is authorized, display the order confirmation page
    return render(request, 'order_confirmation.html', {'order': order})


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