from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from packngoapp.models import booking
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import get_connection, EmailMessage
from django.conf import settings
import random

# Create your views here.

def home(request):
    return render(request, 'home.html')


def index(request):
    
    return render(request, 'index.html')


def user_register(request):
    
    if request.method == "GET":
        
        return render(request, 'register.html')
 
    else:
        
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            
            u = User.objects.create(username = username, first_name = first_name, last_name = last_name,
                                email = email)
            
            u.set_password(password)
            
            u.save()
            
            return HttpResponse("successful")
        
        else:
            
            context = {}
            
            context['error'] = "Password doesnot match confirm password"
            
            return render(request, 'register.html', context)
        
     

def user_login(request):
    
    if request.method == "GET":
        
        return render(request, 'login.html')
    
    else:
        
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username = username, password = password)
        
        if user is not None:
            
            login(request, user)
            
            return redirect('/')
        
        else:
            
            context = {}
            
            context['error'] = "Invalid username or password"
            
            return render(request, 'login.html', context)
        
@login_required(login_url="/user_login")
def user_logout(request):
    
    logout(request)
    
    return redirect('/')      

# def book(request):
#     if request.method == 'GET':
        
    
#         return render(request,'booking.html')
#     else:
        
        
#         name = request.POST['name']
#         quantity = request.POST['quantity']
#         pickup_loc = request.POST['pickup_loc']
#         drop_loc = request.POST['drop_loc']
#         phone_no = request.POST['phone_no']
        
        
#         if quantity == "0-20":
#             price = 2
#         elif quantity == "20-40":
#             price = 4
#         elif quantity == "40-60":
#             price = 6
#         else:
#             price = 0
#         p = booking.objects.create(name=name,quantity=quantity,pickup_loc=pickup_loc,drop_loc=drop_loc,
#                                    phone_no=phone_no, price = price, user = request.user)
#         p.save()
        
#         return redirect('/read_book')
    
    
    
# def booking_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         quantity = request.POST.get('quantity')
#         pickup_loc = request.POST.get('pickup_loc')
#         drop_loc = request.POST.get('drop_loc')
#         phone_no = request.POST.get('phone_no')
#         vehicle = request.POST.get('vehicle')

#         if vehicle:
#             # Process the final booking
#             return HttpResponse(f'Booking confirmed for {vehicle} from {pickup_loc} to {drop_loc}.')
        
#         # Get the available vehicles based on the quantity
#         available_vehicles = VEHICLES.get(quantity, [])

#         return render(request, 'select_vehicle.html', {
#             'name': name,
#             'pickup_loc': pickup_loc,
#             'drop_loc': drop_loc,
#             'phone_no': phone_no,
#             'available_vehicles': available_vehicles
#         })
#     return render(request, 'booking.html')


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import booking

# Assuming a dictionary for available vehicles
VEHICLES = {
    '0-20': ['Small Car', 'Bike'],
    '20-40': ['Sedan', 'SUV'],
    '40-60': ['Truck', 'Van']
}

@login_required(login_url="/user_login")
def book(request):
    if request.method == 'GET':
        return render(request, 'booking.html')
    else:
        # Handle form submission
        name = request.POST['name']
        quantity = request.POST['quantity']
        pickup_loc = request.POST['pickup_loc']
        drop_loc = request.POST['drop_loc']
        phone_no = request.POST['phone_no']

        # Determine price based on quantity
        if quantity == "0-20":
            price = 400
        elif quantity == "20-40":
            price = 800
        elif quantity == "40-60":
            price = 1600
        else:
            price = 0

        # Save booking data to the database
        p = booking.objects.create(
            name=name,
            quantity=quantity,
            pickup_loc=pickup_loc,
            drop_loc=drop_loc,
            phone_no=phone_no,
            price=price,  
            user=request.user
        )
        p.save()

        # Redirect to vehicle selection page
        return redirect('booking_view', booking_id=p.id)


# def booking_view(request, booking_id):
#     # Retrieve the booking based on the ID
#     booking_instance = booking.objects.get(id=booking_id)

#     if request.method == 'POST':
#         vehicle = request.POST.get('vehicle')

#         if vehicle:
#             # Finalize the booking and display a confirmation message
#             booking_instance.vehicle = vehicle
#             booking_instance.save()
#             return HttpResponse(f'Booking confirmed for {vehicle} from {booking_instance.pickup_loc} to {booking_instance.drop_loc}.')

#     # Get the available vehicles based on the quantity
#     available_vehicles = VEHICLES.get(booking_instance.quantity, [])

#     return render(request, 'book.html', {
#         'booking': booking_instance,
#         'available_vehicles': available_vehicles
#     })

# def booking_view(request, booking_id):
#     # Retrieve the booking based on the ID
#     booking_instance = booking.objects.get(id=booking_id)

#     if request.method == 'POST':
#         vehicle = request.POST.get('vehicle')

#         if vehicle:
#             # Finalize the booking and display a confirmation message
#             booking_instance.vehicle = vehicle
#             booking_instance.save()
#             return HttpResponse(f'Booking confirmed for {vehicle} from {booking_instance.pickup_loc} to {booking_instance.drop_loc}.')

#     # Get the available vehicles based on the quantity
#     available_vehicles = VEHICLES.get(booking_instance.quantity, [])
    
#     # Create a list of tuples (vehicle, price)
#     vehicle_prices = [(vehicle, calculate_price(vehicle)) for vehicle in available_vehicles]

#     return render(request, 'book.html', {
#         'booking': booking_instance,
#         'vehicle_prices': vehicle_prices
#     })



from django.shortcuts import render, redirect

def booking_view(request, booking_id):
    # Retrieve the booking based on the ID
    booking_instance = booking.objects.get(id=booking_id)

    if request.method == 'POST':
        vehicle = request.POST.get('vehicle')

        if vehicle:
            # Finalize the booking and save the selected vehicle
            booking_instance.vehicle = vehicle
            booking_instance.save()

            # Redirect to the booking confirmation page
            return redirect('booking_confirmation', booking_id=booking_instance.id)

    # Get the available vehicles based on the quantity
    available_vehicles = VEHICLES.get(booking_instance.quantity, [])
    
    # Create a list of tuples (vehicle, price)
    vehicle_prices = [(vehicle, calculate_price(vehicle)) for vehicle in available_vehicles]

    return render(request, 'book.html', {
        'booking': booking_instance,
        'vehicle_prices': vehicle_prices
    })

def calculate_price(vehicle):
    # Define specific prices for each vehicle type
    prices = {
        'Small Car': 400,
        'Bike': 400,
        'Sedan': 800,
        'SUV': 800,
        'Truck': 1600,
        'Van': 1600
    }
    return prices.get(vehicle, 0)

def calculate_price(vehicle):
    # You can define specific prices for each vehicle type
    prices = {
        'Small Car': 400,
        'Bike': 400,
        'Sedan': 800,
        'SUV': 800,
        'Truck': 1600,
        'Van': 1600
    }
    return prices.get(vehicle, 0)



def booking_confirmation(request, booking_id):
    # Retrieve the booking based on the ID
    booking_instance = booking.objects.get(id=booking_id)
    available_vehicles = VEHICLES.get(booking_instance.quantity, [])
    vehicle_prices = [(vehicle, calculate_price(vehicle)) for vehicle in available_vehicles]

    return render(request, 'booking_confirmation.html', {
        'booking': booking_instance,
        'vehicle_prices': vehicle_prices
    })



@login_required(login_url='/user_login')    
def read_book(request):
    user = request.user
    p = booking.objects.filter(user = user)
    context = {}
    context['data'] = p
    return render(request,'read_book.html', context)

def order_history(request):
    # Fetch all bookings for the current user
    bookings = booking.objects.filter(user=request.user).order_by('-date')
    
    return render(request, 'order_history.html', {
        'bookings': bookings
    })
    

def forgot_password(request):
    
    if request.method == "GET":
        
        return render(request, "forgot_password.html")
    
    else:
        
        email = request.POST['email']
        
        request.session['email'] = email
        
        user = User.objects.filter(email = email).exists()
        
        if user:
        
            otp = random.randint(1000, 9999)
            
            request.session['otp'] = otp
            
            with get_connection(
                host = settings.EMAIL_HOST,
                port = settings.EMAIL_PORT,
                username = settings.EMAIL_HOST_USER,
                password = settings.EMAIL_HOST_PASSWORD,
                user_tls = settings.EMAIL_USE_TLS
            ) as connection :
                
                subject = "OTP Verification"
                email_from = settings.EMAIL_HOST_USER
                reciption_list = [email]
                message = f"OTP is {otp}"
                
                EmailMessage(subject, message, email_from, reciption_list, connection = connection).send()
            return redirect('/otp_verification')
        
        else:
            
            context = {}
            
            context['error'] = "User Not a Found"
            
            return render(request, 'forgot_password.html', context)
        
    
def otp_verification(request):
    
    if request.method == "GET":
        
        return render(request, 'otp.html')
    
    else:
        
        otp = int(request.POST['otp'])
        
        email_otp = int(request.session['otp'])
        
        if otp == email_otp:
            
            return redirect("/new_password")
        
        else:
            
            context = {}
            
            context['error'] = "OTP does not match"
            
            return render(request, 'forgot_password.html', context)
        
        
def new_password(request):
    
    if request.method == "GET":
        
        return render(request, 'new_password.html')
    
    else:
        
        email = request.session['email']
        
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        user = User.objects.get(email = email)
        
        if password == confirm_password:
            
            user.set_password(password)
            
            user.save()
            
            return redirect("/login")
        
        else:
            
            context ={}
            
            context['error'] = "Password and confirm Password does not match"
            
            return render(request, 'new_password.html', context)   
        
        
        



 



    


