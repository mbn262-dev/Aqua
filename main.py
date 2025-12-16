"""
Repository: mobile-app
Branch: main

This file represents production-ready code.
All changes merged here come from Pull Requests
linked to ClickUp tasks.
"""

import hashlib
from uuid import uuid4

from auth import login_user
from metrics import track_event


def mask_username(username: str) -> str:
    """
    CU-372: Mask username so sensitive identifiers are not sent to analytics.
    Uses a short hash for consistency without exposure.
    """
    if not username:
        return "unknown"
    return hashlib.sha256(username.encode("utf-8")).hexdigest()[:10]


def validate_credentials(user_credentials: dict) -> dict:
    """
    Validate credentials and ensure sensitive values are not leaked.
    """
    username = (user_credentials.get("username") or "").strip()
    password = (user_credentials.get("password") or "").strip()

    if not username:
        raise ValueError("Username is required.")
    if not password:
        raise ValueError("Password is required.")

    return {"username": username, "password": password}


def track_login_event(event_name: str, correlation_id: str, username=None, **extra) -> None:
    """
    CU-372: Centralize analytics tracking with masked identifiers.
    """
    payload = {
        "event_name": event_name,
        "correlation_id": correlation_id,
        "user_ref": mask_username(username) if username else None,
        **extra,
    }
    track_event(**payload)


def main():
    """
    Entry point for the application.

    Related ClickUp tasks:
    - CU-372: Mask sensitive login data in analytics
    """

    correlation_id = str(uuid4())

    user_credentials = {
        "username": "test_user@example.com",
        "password": "secure_password",
    }

    try:
        cleaned = validate_credentials(user_credentials)

        track_login_event(
            event_name="login_attempt",
            correlation_id=correlation_id,
            username=cleaned["username"],
        )

        user = login_user(cleaned)

        track_login_event(
            event_name="login_success",
            correlation_id=correlation_id,
            username=cleaned["username"],
            user_id=user["id"],
        )

        print("User logged in successfully.")

    except ValueError as error:
        track_login_event(
            event_name="login_failed",
            correlation_id=correlation_id,
            username=user_credentials.get("username"),
            reason=str(error),
        )
        print(f"Login failed: {error}")

    except Exception as error:
        track_login_event(
            event_name="login_error",
            correlation_id=correlation_id,
            username=user_credentials.get("username"),
            error_type=type(error).__name__,
        )
        print("Unexpected error occurred.")
        raise


if __name__ == "__main__":
    main()
