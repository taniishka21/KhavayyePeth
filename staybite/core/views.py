# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
import csv, os, json
from .forms import UserUpdateForm
from django.conf import settings
from django.db import IntegrityError
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# ✅ Import Gemini
import google.generativeai as genai

# ---------------- Chatbot AI ----------------
from .chatbot_ai import chatbot_api


# ========== GEMINI SETUP ==========
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-2.5-pro")
else:
    gemini_model = None


# from .chatbot_ai import ask_gemini   # import your AI helper
@csrf_exempt
def chatbot_response(request):
    """
    Handles API requests for the chatbot. Expects chat history from the client.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            user_message = data.get("message")
            chat_history = data.get("history", [])  # Get the history from the request
            
            if not user_message:
                return JsonResponse({"reply": "Please provide a message."})

            reply = chatbot_api(user_message, chat_history)
            
            return JsonResponse({"reply": reply})

        except Exception as e:
            return JsonResponse({"reply": f"Sorry, I encountered an error. Please try again. (Error: {str(e)})"}, status=500)
    
    return JsonResponse({"reply": "Invalid request method."}, status=405)


# # ✅ Final Gemini Chatbot View
# @csrf_exempt
# @require_POST
# def chat_api(request):
#     """
#     POST JSON: {"message": "..."}
#     Returns JSON: {"reply": "...", "mode": "gemini|dev|fallback"}
#     """
#     try:
#         payload = json.loads(request.body.decode("utf-8"))
#     except Exception:
#         return JsonResponse({"error": "Invalid JSON"}, status=400)

#     user_message = (payload.get("message") or "").strip()
#     if not user_message:
#         return JsonResponse({"error": "Message is required"}, status=400)

#     # ✅ If Gemini is available, use it
#     if gemini_model:
#         try:
#             system_prompt = (
#                 "You are Khavayye AI, a friendly Pune food guide. "
#                 "Always answer based on Pune restaurants, areas, and cuisines. "
#                 "Keep answers short, helpful, and in bullet points."
#             )
#             response = gemini_model.generate_content(
#                 f"{system_prompt}\n\nUser: {user_message}"
#             )
#             reply = response.text.strip()
#             return JsonResponse({"reply": reply, "mode": "gemini"})
#         except Exception as e:
#             return JsonResponse({
#                 "reply": f"(fallback) You said: {user_message}\n⚠️ Gemini error: {str(e)[:140]}",
#                 "mode": "fallback"
#             }, status=200)

#     # ✅ If no Gemini key, fallback
#     return JsonResponse({
#         "reply": f"(dev) You said: {user_message}",
#         "mode": "dev"
#     })


@login_required
def explore_view(request):
    restaurants = []
    locations = set()
    file_path = os.path.join(settings.BASE_DIR, 'core', 'data', 'zomato_outlet_final.csv')
    
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            cleaned_row = {key: value.strip() for key, value in row.items()}
            restaurants.append(cleaned_row)
            locations.add(cleaned_row['loc']) # Collects unique locations
    
    context = {
        'restaurants': restaurants,
        'locations': sorted(list(locations)), # Pass sorted unique locations to the template
    }
    
    return render(request, 'explore.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('explore')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('explore')

    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.first_name = fullname
            user.save()

            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('explore')
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return redirect('register')

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

def dashboard_view(request):
    return render(request,'dashboard.html')

def home_view(request):
    return render(request,'home.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form
    }
    
    return render(request, 'edit_profile.html', context)

def about_view(request):
    return render(request, 'about.html')

@xframe_options_exempt
def chatbot_view(request):
    return render(request, 'chatbot_app.html')



