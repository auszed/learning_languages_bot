from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)
# Create your views here.

MODEL_SELECTION = "gpt-4.1-nano"

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        response = client.chat.completions.create(
            model= MODEL_SELECTION,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ],
            max_tokens=150
        )
        ai_message = response.choices[0].message.content
        return JsonResponse({'message': ai_message})
    return render(request, 'chatbot_main.html')