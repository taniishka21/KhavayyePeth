from django.urls import path
from . import views  # Assuming your views.py is in the same directory
# from .views import chat_api

urlpatterns = [
    path('', views.home_view, name='home'),
    path('explore/', views.explore_view, name='explore'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('about/', views.about_view, name='about'),
    path("chatbot/", views.chatbot_response, name="chatbot"),
]