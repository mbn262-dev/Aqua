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


def validate_credentials(user_credentials: dict) -> dict:
    username = (user_credentials.get("username") or "").strip()
    password = (user_credentials.get("password") or "").strip()

    if not username:
        raise ValueError("Username is required.")
    if not password:
        raise ValueError("Password is required.")

    return {"username": username, "password": password}


def map_login_error_to_code(error: Exception) -> str:
    """
    CU-381: Standardize error reasons for clearer UX and better reporting.
    """
    if isinstance(error, ValueError):
        # Common validation errors
        message = str(error).lower()
        if "username" in message:
            return "MISSING_USERNAME"
        if "password" in message:
            return "MISSING_PASSWORD"
        return "INVALID_INPUT"

    if isinstance(error, PermissionError):
        return "INVALID_CREDENTIALS"

    if isinstance(error, TimeoutError):
        return "TIMEOUT"

    return "UNKNOWN_ERROR"


def user_friendly_message(error_code: str) -> str:
    """
    CU-381: Provide consistent messages without exposing sensitive details.
    """
    messages = {
        "MISSING_USERNAME": "Please enter your username.",
        "MISSING_PASSWORD": "Please enter your password.",
        "INVALID_INPUT": "Please check your login details and try again.",
        "INVALID_CREDENTIALS": "Incorrect username or password.",
        "TIMEOUT": "Login is taking longer than expected. Please try again.",
        "UNKNOWN_ERROR": "Something went wrong. Please try again.",
    }
    return messages.get(error_code, messages["UNKNOWN_ERROR"])


def track_login_event(event_name: str, correlation_id: str, user_id=None, **extra) -> None:
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
    - CU-381: Clearer login error messages and standardized error reasons
    """
    correlation_id = str(uuid4())

    user_credentials = {
        "username": "test_user",
        "password": "secure_password",
    }

    try:
        cleaned = validate_credentials(user_credentials)

        track_login_event(
            event_name="login_attempt",
            correlation_id=correlation_id,
        )

        user = login_user(cleaned)

        track_login_event(
            event_name="login_success",
            correlation_id=correlation_id,
            user_id=user["id"],
        )

        print("User logged in successfully.")

    except Exception as error:
        error_code = map_login_error_to_code(error)

        # CU-381: Track standardized reason instead of raw message
        track_login_event(
            event_name="login_failed",
            correlation_id=correlation_id,
            error_code=error_code,
        )

        # CU-381: Show a friendly message to the user
        print(user_friendly_message(error_code))


if __name__ == "__main__":
    main()
