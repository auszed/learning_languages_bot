from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model # authentification for passwords save
from django.core.exceptions import ValidationError

class CreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='First Name',
        help_text='Optional.',
        widget=forms.TextInput(
            attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Enter your first name'
            }
        )
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Last Name',
        help_text='Optional.',
        widget=forms.TextInput(
            attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Enter your last name'
            }
        )
    )
    email = forms.EmailField(
        max_length=254,
        label='Email',
        help_text='Required. Inform a valid email address.',
        widget=forms.EmailInput(
            attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Enter your email'
            }
        )
    )
    terms_agreement = forms.BooleanField(
        required=True,
        label='I agree to the terms and conditions',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-checkbox h-4 w-4 text-[#ffe599] rounded focus:ring-[#ffe599]'
            }
        )
    )

    # password confirm
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Enter your password'
            }
        ),
        strip=False,
        help_text='Enter your password',
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Confirm your password'
            }
        ),
        strip=False,
        help_text='Confirm your password',
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'placeholder': 'Enter your password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'placeholder': 'Confirm your password'
        })
        self.fields['username'].widget.attrs.update({
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'placeholder': 'Choose a username'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


 
        # <label for="password">Password:</label><br>
        # <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"  type="password" id="password" name="password"><br><br>
        # <label for="confirm_password">Confirm Password:</label><br>
        # <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"  type="password" id="confirm_password" name="confirm_password"><br><br>
        # <input type="checkbox" id="terms_agreement" name="terms_agreement">
        # <label for="terms_agreement">I agree to the Terms of Service and Privacy Policy</label><br><br>
        # <input type="submit" value="Create Account">