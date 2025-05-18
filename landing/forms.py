from django import forms
from django.contrib.auth.models import User # Using Django's built-in User model
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'placeholder': 'Enter first name'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'placeholder': 'Enter last name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'placeholder': 'you@example.com'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'placeholder': '********'
        }),
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'placeholder': '********'
        }),
        required=True,
        label="Confirm Password"
    )
    terms_agreement = forms.BooleanField(
        required=True,
        label="I agree to the Terms of Service and Privacy Policy",
        widget=forms.CheckboxInput(attrs={'class': 'mr-2 leading-tight'}) # Add any specific checkbox classes if needed
    )

    class Meta:
        model = User
        # The default User model requires a username.
        # If you want to use email as the username, you'd typically create a custom User model.
        # For now, let's add 'username' and you can decide how to populate it
        # (e.g., make it same as email, or add another field to your HTML).
        # Or, you can make the username field not required in the form and populate it in the view.
        fields = ['first_name', 'last_name', 'email'] # We'll handle username and password separately for clarity

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return confirm_password

    # You can add a clean_username method if you decide to add a username field to the form
    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if User.objects.filter(username=username).exists():
    #         raise ValidationError("This username is already taken.")
    #     return username

    def save(self, commit=True):
        user = super().save(commit=False)
        # If you don't have a username field in your form, you need to set it.
        # A common practice is to use the email as the username,
        # ensure your User model (if custom) or logic supports this.
        # For the default User model, username is required and unique.
        user.username = self.cleaned_data['email'] # Example: using email as username
        user.set_password(self.cleaned_data['password']) # Hashes the password
        if commit:
            user.save()
        return user