from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.http import HttpResponseForbidden
from django.contrib import messages
from .google_service import authorization_url, fetch_credentials_from_request

def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserRegisterForm()

    return render(request, "accounts/signup.html", {"form": form})


@login_required
def dashboard(request):
    if request.user.is_doctor():
        return redirect("doctor_dashboard")
    return redirect("patient_dashboard")


@login_required
def google_connect(request):
    if not request.user.is_doctor():
        return HttpResponseForbidden("Doctor access only")

    auth_url, state = authorization_url(request)
    if not auth_url:
        messages.error(request, "Google OAuth is not configured on the server.")
        return redirect("doctor_dashboard")

    # Save state in session for verification in callback
    request.session["oauth_state"] = state
    return redirect(auth_url)


@login_required
def google_callback(request):
    if not request.user.is_doctor():
        return HttpResponseForbidden("Doctor access only")

    # Verify state if present
    state = request.session.get("oauth_state")
    if state and request.GET.get("state") != state:
        messages.error(request, "Invalid OAuth state")
        return redirect("doctor_dashboard")

    creds = fetch_credentials_from_request(request)
    if not creds:
        messages.error(request, "Failed to fetch Google credentials")
        return redirect("doctor_dashboard")

    # Save tokens into user model
    request.user.google_access_token = creds.token
    # refresh_token may be None if previously granted; only set if present
    if getattr(creds, "refresh_token", None):
        request.user.google_refresh_token = creds.refresh_token
    request.user.google_token_expiry = creds.expiry
    request.user.save(update_fields=["google_access_token", "google_refresh_token", "google_token_expiry"])

    messages.success(request, "Google Calendar connected successfully.")
    return redirect("doctor_dashboard")



