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


DEFAULT_SESSION_DAYS = 1
REMEMBER_ME_SESSION_DAYS = 30


def get_session_days(remember_me: bool) -> int:
    """
    CU-360: Define session duration based on 'remember me' selection.
    """
    return REMEMBER_ME_SESSION_DAYS if remember_me else DEFAULT_SESSION_DAYS


def validate_credentials(user_credentials: dict) -> dict:
    """
    Validate credentials so empty fields don't cause crashes downstream.
    Returns cleaned credentials + remember_me flag.
    """
    username = (user_credentials.get("username") or "").strip()
    password = (user_credentials.get("password") or "").strip()
    remember_me = bool(user_credentials.get("remember_me", False))

    if not username:
        raise ValueError("Username is required.")
    if not password:
        raise ValueError("Password is required.")

    return {"username": username, "password": password, "remember_me": remember_me}


def track_login_event(event_name: str, correlation_id: str, user_id=None, **extra) -> None:
    """
    Centralize analytics tracking for login events.
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
    - CU-360: Add 'Remember Me' option + session duration analytics
    """

    correlation_id = str(uuid4())

    # CU-360: Add remember_me as a user preference (default False)
    user_credentials = {
        "username": "test_user",
        "password": "secure_password",
        "remember_me": True,
    }

    try:
        cleaned = validate_credentials(user_credentials)

        # CU-360: Set session duration based on remember_me
        session_days = get_session_days(cleaned["remember_me"])

        # Track attempt with session context
        track_login_event(
            event_name="login_attempt",
            correlation_id=correlation_id,
            remember_me=cleaned["remember_me"],
            session_days=session_days,
        )

        # In a real system, login_user might accept session duration or token policy
        user = login_user(
            {"username": cleaned["username"], "password": cleaned["password"]}
        )

        track_login_event(
            event_name="login_success",
            correlation_id=correlation_id,
            user_id=user["id"],
            remember_me=cleaned["remember_me"],
            session_days=session_days,
        )

        print(f"User logged in successfully. session_days={session_days}")

    except ValueError as error:
        track_login_event(
            event_name="login_failed",
            correlation_id=correlation_id,
            reason=str(error),
        )
        print(f"Login failed: {error}")

    except Exception as error:
        track_login_event(
            event_name="login_error",
            correlation_id=correlation_id,
            error_type=type(error).__name__,
        )
        print("Unexpected error occurred.")
        raise


if __name__ == "__main__":
    main()
