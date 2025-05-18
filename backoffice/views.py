from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse # For cleaner redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, get_user_model
from django.contrib import messages # For user feedback

# models load
from .models import UserProfile, Settings, LanguageModel
# get the user model with the user and password
User = get_user_model() 

# llm import
from openai import OpenAI

# languages availables
from .llm_languages import LANGUAGES

# importing the prompts
from .prompt_engineer.system_prompt import SYSTEM_PROMPT

# open ai keys
client = OpenAI(api_key=settings.OPENAI_API_KEY)
MODEL_SELECTION = "gpt-4.1-nano"

# Variables
MAX_TOKENS = 200

# -----------------------
# chat endpoints
# -----------------------

@login_required
@csrf_exempt
def chat_view(request):
    """view of the main chat"""
    url_name = request.resolver_match.url_name
    print(f"The matched URL name is: {url_name}")

    # You might want to pass user-specific settings to the chat view
    context = {}
    if request.user.is_authenticated:
        try:
            user_settings = Settings.objects.get(user=request.user)
            context['user_preferred_language'] = user_settings.preferred_language
            # Pass other settings if needed by chatbot_main.html
        except Settings.DoesNotExist:
            context['user_preferred_language'] = 'en' # Default
    else:
        context['user_preferred_language'] = 'en' # Default for anonymous users

    return render(request, 'chatbot_main.html', context)

@login_required
@csrf_exempt # If called via AJAX/Fetch from your JS, ensure CSRF is handled appropriately
def translation_user_message(request):
    if request.method == 'POST':
        user_message_translation = request.POST.get('message_translation', "")
        # The 'language' POST parameter is the TARGET language for translation here
        target_language_code = request.POST.get('language', "")

        if not target_language_code:
            return JsonResponse({'error': 'Target language not specified.'}, status=400)

        # Get the language name for the prompt (e.g., "Spanish" from "es")
        target_language_name = dict(LANGUAGES).get(target_language_code, target_language_code) # Fallback to code if name not found

        system_prompt = f"Translate the following message to {target_language_name}."
        try:
            response = client.chat.completions.create(
                model=MODEL_SELECTION,
                temperature=0.8,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message_translation},
                ],
                max_tokens=MAX_TOKENS
            )
            ai_message = response.choices[0].message.content
            return JsonResponse({'message': ai_message})
        except Exception as e:
            return JsonResponse({'error': f'OpenAI API error: {str(e)}'}, status=500)
    # Return an error or appropriate response if not POST
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@login_required
@csrf_exempt
def response_ai_message(request):
    if request.method == 'POST':
        user_message_for_ai = request.POST.get('message_translation', "") # This is the user's input for the AI
        # This 'language' POST parameter is the language the user wants the AI's final response in
        target_response_language_code = request.POST.get('language', "")

        if not target_response_language_code:
            try:
                # Default to user's preferred_language from settings if not specified in request
                user_settings = Settings.objects.get(user=request.user)
                target_response_language_code = user_settings.preferred_language
            except Settings.DoesNotExist:
                target_response_language_code = 'english' # Absolute fallback

        target_response_language_name = dict(LANGUAGES).get(target_response_language_code, target_response_language_code)

        try:
            # 1. Get base response from AI 
            ai_base_response = client.chat.completions.create(
                model=MODEL_SELECTION,
                temperature=0.8,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT}, # SYSTEM_PROMPT might need to be language aware
                    {"role": "user", "content": user_message_for_ai},
                ],
                max_tokens=MAX_TOKENS
            )
            ai_message_content = ai_base_response.choices[0].message.content

            # 2. Translate AI's base response to the user's desired language
            if target_response_language_code.lower() != 'english': 
                translation_prompt_for_ai_response = f"Translate the following message to {target_response_language_name}."
                response_translation = client.chat.completions.create(
                    model=MODEL_SELECTION,
                    temperature=0.8,
                    messages=[
                        {"role": "system", "content": translation_prompt_for_ai_response},
                        {"role": "user", "content": ai_message_content},
                    ],
                    max_tokens=MAX_TOKENS
                )
                ai_message_translated = response_translation.choices[0].message.content
            else:
                ai_message_translated = ai_message_content 

            return JsonResponse({
                'message': ai_message_content, # Potentially the original AI response
                'message_translation': ai_message_translated # The response translated for the user
            })
        except Exception as e:
            return JsonResponse({'error': f'OpenAI API error: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


# -----------------------
# profile views
# -----------------------
@login_required
@csrf_exempt
def profile_view(request):
    """
    Handles viewing and updating UserProfile and Settings.
    """
    # Get or create UserProfile and Settings for the logged-in user
    # This ensures these objects exist.
    user_profile, profile_created = UserProfile.objects.get_or_create(user=request.user)
    user_settings, settings_created = Settings.objects.get_or_create(user=request.user)


    if request.method == 'POST':
        # --- Update UserProfile ---
        user_profile.location = request.POST.get('location', user_profile.location) # Keep old if not provided
        if 'profile_picture' in request.FILES:
            user_profile.profile_picture = request.FILES['profile_picture']
        user_profile.save()

        # --- Update Settings ---
        user_settings.subscription_plan = request.POST.get('subscription_plan', user_settings.subscription_plan)
        user_settings.preferred_language = request.POST.get('preferred_language', user_settings.preferred_language)

        # Handle ManyToManyField for language_learning
        selected_language_codes = request.POST.getlist('language_learning') # .getlist for multiple values
        
        user_settings.language_learning.clear() # Clear existing selections
        for lang_code in selected_language_codes:
            try:
                language_to_add = LanguageModel.objects.get(code=lang_code)
                user_settings.language_learning.add(language_to_add)
            except LanguageModel.DoesNotExist:
                messages.warning(request, f"Could not find language with code: {lang_code}. Please ensure it exists in the system.")
        
        user_settings.save()

        messages.success(request, 'Your profile and settings have been updated successfully!')
        return HttpResponseRedirect(reverse('profile_view')) # Redirect to the same page (PRG pattern)

    # For GET request (or if POST had errors and re-renders)
    all_learning_languages = LanguageModel.objects.all() # For the 'language_learning' multi-select

    context = {
        'user_profile': user_profile,
        'user_settings': user_settings,
        'LANGUAGES_CHOICES': LANGUAGES,  # For the 'preferred_language' select (from your llm_languages.py)
        'SUBSCRIPTION_CHOICES': Settings._meta.get_field('subscription_plan').choices, # Get choices from model
        'ALL_LEARNING_LANGUAGES': all_learning_languages, # For the multi-select
        'SELECTED_LEARNING_LANGUAGES_CODES': [lang.code for lang in user_settings.language_learning.all()] # For pre-selecting in template
    }
    return render(request, "profile.html", context)
    

@login_required
def logout_view(request):
    """
    View to handle user logout.
    """
    # logout(request)  # Log the user out
    messages.info(request, "You have been successfully logged out.")
    return redirect('home')  # Redirect to the home page (or any other page you want)
