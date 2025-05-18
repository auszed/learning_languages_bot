from django.db import models
from django.contrib.auth.models import User

# llm_languages file
from .llm_languages import LANGUAGES


class UserProfile(models.Model):
    """
    Model representing the user profile, extending the base User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    location = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    def __str__(self):
        return self.user.username


class LanguageModel(models.Model):
    """
    Model representing a language. This is needed for the ManyToManyField.
    """
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Settings(models.Model):
    """
    Model representing user settings.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    subscription_plan = models.CharField(
        max_length=20,
        choices=[
            ('Free', 'Free'),
            ('basic', 'Basic'),
            ('premium', 'Premium'),
        ],
        default='basic',
    )
    language_learning = models.ManyToManyField(
        LanguageModel,
        blank=True,  # Allow no languages to be selected initially
    )
    preferred_language = models.CharField(  # Renamed for clarity
        max_length=20,
        choices=LANGUAGES,
        default='en',  # Using 'en' (English code) as a safer default
    )
    
    def __str__(self):
        return self.user.username
