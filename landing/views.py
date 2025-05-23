from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# login auth setup
from django.contrib.auth import get_user_model, login

from django.http import HttpResponse

# model template
from .models import NewUserAccount

# import the forms template
from .forms import UserRegistrationForm

# Create your views here.
def index(request):
    """index website"""
    return render(request, 'index.html')

def pre_order(request):
    """landing page for the pre launch of the product"""
    return render(request, 'preorder.html')

def signin(request):
    """signin to the backoffice"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Attempting signin with email: {email}")
        print(f"Password provided: {'<present>' if password else '<empty>'}")
        user = authenticate(request, username=email, password=password)
        
        print(f"Authentication result: {user}")
        if user is not None:
            print("User authenticated successfully.")
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            print("Redirecting to portal:chatbot")
            return redirect('portal:chatbot')  # Redirect to backoffice
        else:
            print("Authentication failed.")
            messages.error(request, "Invalid email or password. Please try again.")
    
    return render(request, 'signin.html')

def sign_up_new(request):
    if request.user.is_authenticated: # If user is already logged in, redirect them
        return redirect('portal:chatbot') # Redirect to backoffice

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Log the user in immediately after registration
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f"Account created successfully for {user.email}! You are now logged in.")
                return redirect('portal:chatbot') # Redirect to backoffice
            except Exception as e:
                messages.error(request, f"An error occurred during registration: {e}")
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                         error_messages.append(f"{error}")
                    else:
                        error_messages.append(f"{form.fields[field].label or field.replace('_', ' ').title()}: {error}")
            if error_messages:
                messages.error(request, "Please correct the errors below: " + "; ".join(error_messages))
            else:
                messages.error(request, "There was an issue with your submission. Please check the details and try again.")

    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
        'current_page': 'register'
    }
    return render(request, 'sign_up_new.html', context)



# def sign_up_new(request):
#     """sign_up_new to the backoffice"""
   
#     if request.method == 'POST':
#         # Get data from the form
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
#         terms_agreement = request.POST.get('terms_agreement') # This will be 'on' if checked


#         # Basic validation (you should use Django forms for real projects)
#         if not first_name or not last_name or not email or not password or not confirm_password or not terms_agreement:
#             messages.error(request, "All fields are required.")
#             return render(request, 'sign_up_new.html')
            
#         if password != confirm_password:
#             messages.error(request, "Passwords do not match.")
#             return render(request, 'sign_up_new.html')

#         if len(password) < 8:  # Example password complexity rule
#             messages.error(request, "Password must be at least 8 characters long.")
#             return render(request, 'sign_up_new.html')
        
#         if NewUserAccount.objects.filter(email=email).exists():
#             messages.error(request, "Email address is already in use.")
#             return render(request, 'sign_up_new.html')

#         # Convert the terms agreement checkbox value to a boolean
#         terms_agreement_bool = terms_agreement == 'on'

#         # Create a new UserAccount object and save it to the database
#         try:
#             user = NewUserAccount(
#                 first_name=first_name,
#                 last_name=last_name,
#                 email=email,
#                 password=make_password(password),  # Hash the password!
#                 terms_agreement=terms_agreement_bool,
#             )
#             user.save()
#             messages.success(request, "Registration successful!  You can now log in.")
#             return redirect('home')  # Redirect to the login page (create this URL)
#         except Exception as e:
#             messages.error(request, f"An error occurred during registration: {e}")
#             return render(request, 'sign_up_new.html')

#     else:
#         # If it's a GET request, just display the registration form
#         return render(request, 'sign_up_new.html')