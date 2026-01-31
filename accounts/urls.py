from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup, dashboard, google_connect, google_callback

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("google/connect/", google_connect, name="google_connect"),
    path("google/callback/", google_callback, name="google_callback"),
    
]

