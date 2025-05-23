from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import RedirectView

from .forms import CreationForm

class RootRedirectView(RedirectView):
    url = reverse_lazy('registration:signup')

def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Attempting login with email: {email}")
        print(f"Password provided: {'<present>' if password else '<empty>'}")
        
        # Try to find user by email
        # Try to find user by email
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None
        
        print(f"Authentication result: {user}")
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('portal:chatbot')  # Redirect to chatbot page after login
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'registration/login.html')

class SignUpView(CreateView):
    form_class = CreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('portal:chatbot')  # Redirect to chatbot page after signup

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Account created successfully!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)