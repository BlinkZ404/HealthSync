from django.shortcuts import render, redirect , get_object_or_404
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Address
from .models import Donation
from django.contrib.auth import logout
from .models import BloodDonor, Doctor , AvailableDate, AvailableTime , Appointment

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
    appointments = request.user.appointments.all()

    # Pass user and profile data to the template
    return render(request, 'user_profile.html', {
        'user': request.user,
        'profile': profile ,
        'appointments': appointments,
    })

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


# Add a new address for the authenticated user
def add_address(request):
    if request.method == 'POST':
        address_name = request.POST.get('address_name')
        address_number = request.POST.get('address_number')
        address_road = request.POST.get('address_road')

        # Create an Address object linked to the user
        Address.objects.create(user=request.user, name=address_name, number=address_number, road=address_road)
        messages.success(request, "Address added successfully.")
        return redirect('user_profile')  # Redirect back to profile page

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

# Render the Doctors page

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


# doctors views

def doctors(request):
    # Get filter parameters from the request
    gender = request.GET.get('gender')
    specialty = request.GET.get('specialty')
    division = request.GET.get('division')

    # Filter queryset based on parameters
    doctors = Doctor.objects.all()
    if gender:
        doctors = doctors.filter(gender=gender)
    if specialty:
        doctors = doctors.filter(specialty=specialty)
    if division:
        doctors = doctors.filter(division=division)

    # Split expertise into list for displaying badges
    for doctor in doctors:
        doctor.expertise_list = doctor.expertise.split(',')

    return render(request, 'doctors.html', {'doctors': doctors})


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

# Edit the appointment
def edit_appointment(request, appointment_id):
    # Retrieve the appointment for the logged-in user by checking the patient field
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)

    if request.method == 'POST':
        # Get form data
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        patient_name = request.POST.get('patient_name')
        phone_number = request.POST.get('phone_number')
        # blood_group = request.POST.get('blood_group')
        # disease_description = request.POST.get('disease_description')

        # Parse the appointment date to ensure it's in the correct format
        try:
            # Parse and format date and time if needed

            formatted_time = datetime.strptime(appointment_time, "%H:%M").time()
            appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid  format. Please use valid format ")
            return redirect('edit_appointment', appointment_id=appointment_id)

        # Validate the chosen date and time
        if (appointment_date and appointment_time) and \
                appointment.doctor.available_dates.filter(date=appointment_date).exists() and \
                appointment.doctor.available_times.filter(time=appointment_time).exists():

            # Update appointment details
            appointment.appointment_date = appointment_date
            appointment.appointment_time = formatted_time
            appointment.patient_name = patient_name
            appointment.phone_number = phone_number
            # appointment.blood_group = blood_group
            # appointment.disease_description = disease_description
            appointment.save()

            messages.success(request, "Appointment updated successfully.")
            return redirect('user_profile')
        else:
            messages.error(request, "Please choose a date and time from the available options.")

    # Get available dates and times for the doctor's schedule
    available_dates = appointment.doctor.available_dates.all()

    # Format available times as HH:MM strings for the dropdown
    available_times = [time.time.strftime("%H:%M") for time in appointment.doctor.available_times.all()]

    return render(request, 'edit_appointment.html', {
        'appointment': appointment,
        'available_dates': available_dates,
        'available_times': available_times,
    })

# Cancel appointment
def cancel_appointment(request, appointment_id):
    # Retrieve the appointment and ensure it belongs to the logged-in user
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)

    # Update the status to 'canceled' instead of deleting
    appointment.status = 'canceled'
    appointment.save()

    messages.success(request, "Appointment has been canceled.")
    return redirect('user_profile')

#get the available date and time from the admin to the user
def get_available_slots(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    available_dates = list(doctor.available_dates.values_list('date', flat=True))
    available_times = list(doctor.available_times.values_list('time', flat=True))
    return JsonResponse({
        'available_dates': available_dates,
        'available_times': [time.strftime('%H:%M') for time in available_times]
    })