"""
Repository: mobile-app
Branch: main

This file represents production-ready code.
All changes merged here come from Pull Requests
linked to ClickUp tasks.
"""

import time
from uuid import uuid4

from auth import login_user
from metrics import track_event


LOGIN_MAX_ATTEMPTS = 3
LOGIN_RETRY_BACKOFF_SECONDS = 0.25
LOGIN_RETRYABLE_ERRORS = (TimeoutError, ConnectionError)


def normalize_username(username: str) -> str:
    """
    CU-341: Normalize input so minor formatting issues don't cause login failures.
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
    Adds correlation_id to link attempt/success/failure/error.
    """
    payload = {
        "event_name": event_name,
        "user_id": user_id,
        "correlation_id": correlation_id,
        **extra,
    }
    track_event(**payload)


def login_with_retries(credentials: dict, correlation_id: str) -> dict:
    """
    CU-341: Retry login on transient errors (timeouts/network issues).
    CU-350: Track attempts and timing.
    """
    start = time.time()

    for attempt in range(1, LOGIN_MAX_ATTEMPTS + 1):
        try:
            track_login_event(
                event_name="login_attempt",
                correlation_id=correlation_id,
                attempt=attempt,
                max_attempts=LOGIN_MAX_ATTEMPTS,
            )

            user = login_user(credentials)

            duration_ms = int((time.time() - start) * 1000)
            track_login_event(
                event_name="login_success",
                correlation_id=correlation_id,
                user_id=user["id"],
                attempt=attempt,
                duration_ms=duration_ms,
            )
            return user

        except LOGIN_RETRYABLE_ERRORS as error:
            # Transient error: retry (unless this was last attempt)
            if attempt == LOGIN_MAX_ATTEMPTS:
                duration_ms = int((time.time() - start) * 1000)
                track_login_event(
                    event_name="login_error",
                    correlation_id=correlation_id,
                    error_type=type(error).__name__,
                    attempt=attempt,
                    duration_ms=duration_ms,
                )
                raise

            time.sleep(LOGIN_RETRY_BACKOFF_SECONDS * attempt)

    # Should be unreachable, but keeps static analyzers happy
    raise RuntimeError("Login retry loop ended unexpectedly.")


def main():
    """
    Entry point for the application.

    Related ClickUp tasks:
    - CU-341: Fix Android login crash
    - CU-350: Add login success analytics event
    """
    correlation_id = str(uuid4())

    user_credentials = {
        "username": "test_user",
        "password": "secure_password",
    }

    try:
        # CU-341: Validate + clean before attempting login
        cleaned_credentials = validate_credentials(user_credentials)

        # CU-341/CU-350: Login with retries and richer analytics
        user = login_with_retries(cleaned_credentials, correlation_id)

        print(f"User logged in successfully. user_id={user['id']}")

    except ValueError as error:
        # Validation failures (expected)
        track_login_event(
            event_name="login_failed",
            correlation_id=correlation_id,
            reason=str(error),
        )
        print(f"Login failed: {error}")

    except Exception as error:
        # Unexpected errors
        track_login_event(
            event_name="login_error",
            correlation_id=correlation_id,
            error_type=type(error).__name__,
        )
        print("Unexpected error occurred.")
        raise


if __name__ == "__main__":
    main()
