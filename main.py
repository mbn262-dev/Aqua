"""
Repository: mobile-app
Branch: main

This file represents production-ready code.
All changes merged here come from Pull Requests
linked to ClickUp tasks.
"""

from auth import login_user
from metrics import track_event


def main():
    """
    Entry point for the application.

    Related ClickUp tasks:
    - CU-341: Fix Android login crash
    - CU-350: Add login success analytics event
    """

    user_credentials = {
        "username": "test_user",
        "password": "secure_password"
    }

    try:
        # CU-341: Fixed crash when password field is empty
        user = login_user(user_credentials)

        # CU-350: Track successful login event
        track_event(
            event_name="login_success",
            user_id=user["id"]
        )

        print("User logged in successfully.")

    except ValueError as error:
        # Expected validation errors (handled gracefully)
        print(f"Login failed: {error}")

    except Exception as error:
        # Unexpected errors
        print("Unexpected error occurred.")
        raise error


if __name__ == "__main__":
    main()
