"""
Repository: mobile-app
Branch: main

This file represents production-ready code.
All changes merged here come from Pull Requests
linked to ClickUp tasks.
"""

from uuid import uuid4

from auth import login_user
from metrics import track_event


def normalize_username(username: str) -> str:
    """
    CU-341: Normalize input so minor formatting issues don't cause login failures.
    - trims whitespace
    - lowercases for consistency (adjust if your system is case-sensitive)
    """
    return (username or "").strip().lower()


def validate_credentials(user_credentials: dict) -> dict:
    """
    CU-341: Validate credentials so empty fields don't cause crashes downstream.
    Returns a cleaned credentials dict.
    """
    username = normalize_username(user_credentials.get("username"))
    password = (user_credentials.get("password") or "").strip()

    if not username:
        raise ValueError("Username is required.")
    if not password:
        raise ValueError("Password is required.")

    return {"username": username, "password": password}


def track_login_event(event_name: str, correlation_id: str, user_id=None, **extra) -> None:
    """
    CU-350: Centralize analytics tracking for login events.
    Adds a correlation_id to link attempts with outcomes.
    """
    payload = {
        "event_name": event_name,
        "user_id": user_id,
        "correlation_id": correlation_id,
        **extra,
    }
    track_event(**payload)


def main():
    """
    Entry point for the application.

    Related ClickUp tasks:
    - CU-341: Fix Android login crash
    - CU-350: Add login success analytics event
    """
    # CU-350: Correlation ID ties attempt/success/failure together in analytics
    correlation_id = str(uuid4())

    user_credentials = {
        "username": "test_user",
        "password": "secure_password"
    }

    try:
        # CU-341: Validate + clean before attempting login
        cleaned_credentials = validate_credentials(user_credentials)

        # CU-350: Track login attempt (optional but useful)
        track_login_event(
            event_name="login_attempt",
            correlation_id=correlation_id
        )

        user = login_user(cleaned_credentials)

        # CU-350: Track successful login event
        track_login_event(
            event_name="login_success",
            correlation_id=correlation_id,
            user_id=user["id"]
        )

        print("User logged in successfully.")

    except ValueError as error:
        # CU-350: Track failed login attempt with reason
        track_login_event(
            event_name="login_failed",
            correlation_id=correlation_id,
            reason=str(error)
        )
        print(f"Login failed: {error}")

    except Exception as error:
        # Unexpected errors: track and re-raise
        track_login_event(
            event_name="login_error",
            correlation_id=correlation_id,
            error_type=type(error).__name__
        )
        print("Unexpected error occurred.")
        raise


if __name__ == "__main__":
    main()

