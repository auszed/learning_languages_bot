from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages

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
    return render(request, 'signin.html')

def sign_up_new(request):
    if request.user.is_authenticated: # If user is already logged in, redirect them
        return redirect('home') # Or a dashboard page

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Optional: Log the user in immediately after registration
                login(request, user, backend='django.contrib.auth.backends.ModelBackend') # Specify backend
                messages.success(request, f"Account created successfully for {user.email}! You are now logged in.")
                return redirect('home') # Redirect to home page or a 'welcome' page
            except Exception as e:
                # This is a general catch, specific errors should be handled by form validation
                messages.error(request, f"An error occurred during registration: {e}")
        else:
            # Form is not valid, errors will be bound to the form instance
            # and can be displayed in the template.
            # Create a single message for all form errors for simplicity, or let the template handle field errors.
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__': # Non-field errors
                         error_messages.append(f"{error}")
                    else:
                        error_messages.append(f"{form.fields[field].label or field.replace('_', ' ').title()}: {error}")
            if error_messages:
                messages.error(request, "Please correct the errors below: " + "; ".join(error_messages))
            else: # Fallback generic error
                messages.error(request, "There was an issue with your submission. Please check the details and try again.")


    else: # For a GET request
        form = UserRegistrationForm()

    # Prepare context to pass to the template
    # We pass the original request.POST data back to the template on POST if there are errors,
    # so the form fields can be re-populated. Django forms handle this automatically when you pass `form` instance.
    context = {
        'form': form,
        'current_page': 'register' # For highlighting active nav link, if needed
    }
    # Assuming your registration template is named 'registration/register.html' or similar
    # and is in a 'templates/registration/' directory within your app or project's templates folder.
    # Your template extends 'base.html' and is in the root of your templates dir for the app.
    # Let's assume your template file is named `preorder_form.html` (based on your css `style_preorder.css`)
    # or you create a new one like `register.html`.
    # For this example, let's say the template you provided is `account/register.html`
    return render(request, 'sign_up_new.html', context) # Update 'account/register.html' to your actual template path



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