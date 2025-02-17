from django.shortcuts import render
from django.http import JsonResponse
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)

# Configure Gemini AI with your API key
gemini_api_key = "AIzaSyA4pUQUbLWSnDciHbDQkstkSxyKrlovAPU"
genai.configure(api_key=gemini_api_key)

# Initialize the model
model_name = "gemini-1.5-flash"
model = genai.GenerativeModel(model_name)

def ask_gemini(message):
    """
    Generate a response using Gemini AI.
    """
    try:
        # Generate content with the specified message
        response = model.generate_content(message)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error communicating with Gemini AI: {e}")
        return "Error: Unable to process your request at this time. Please try again later."

def chatbot(request):
    """
    Handle chatbot requests.
    """
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        if not message:
            logger.error("Received an empty message in the POST request.")
            return JsonResponse({'error': 'Message cannot be empty.'}, status=400)

        logger.debug(f"POST request received. Message: {message}")
        response = ask_gemini(message)
        logger.debug(f"Response: {response}")
        return JsonResponse({'message': message, 'response': response})

    logger.debug("GET request received.")
    return render(request, 'chatbot.html')
