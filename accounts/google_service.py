import os
from django.urls import reverse
from google_auth_oauthlib.flow import Flow


SCOPES = ["https://www.googleapis.com/auth/calendar"]


def _client_config():
    """Build client config from environment variables.

    Requires `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` to be set in env.
    """
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    if not client_id or not client_secret:
        return None

    return {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }


def build_flow(request):
    """Create a Flow instance with redirect URI set for this request."""
    config = _client_config()
    if not config:
        return None

    redirect_uri = request.build_absolute_uri(reverse("google_callback"))
    flow = Flow.from_client_config(config, scopes=SCOPES)
    flow.redirect_uri = redirect_uri
    return flow


def authorization_url(request):
    """Returns (auth_url, state) for redirecting the user to Google's consent screen."""
    flow = build_flow(request)
    if not flow:
        return None, None
    auth_url, state = flow.authorization_url(access_type="offline", include_granted_scopes="true", prompt="consent")
    return auth_url, state


def fetch_credentials_from_request(request):
    """Exchange the OAuth callback request for credentials (google.oauth2.credentials.Credentials).

    Caller should handle saving credentials to user model.
    """
    flow = build_flow(request)
    if not flow:
        return None

    # The authorization response is the full URL with code & state
    auth_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=auth_response)
    return flow.credentials
