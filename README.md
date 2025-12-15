# Example: ClickUp ↔ GitHub Integration (main.py)

This repository contains a **simple, concrete example** that demonstrates how a **ClickUp task flows through GitHub** and ultimately lands as **production-ready code in the `main` branch**.

The focus of this repo is the `main.py` file, which represents **completed, reviewed, and released work**.

---

## What This Example Demonstrates

This example shows:

* How ClickUp tasks are referenced in code
* How multiple tasks can contribute to a single file
* How GitHub branches, commits, and PRs roll up into `main`
* How `main` reflects finished ClickUp work

---

## The `main` Branch

The `main` branch is **protected** and contains only:

* Reviewed code
* Approved pull requests
* Completed ClickUp tasks

There are **no direct commits** to `main`.

All changes arrive via Pull Requests that reference ClickUp task IDs.

---

## main.py (Production Example)

The `main.py` file is the entry point of the application.

It includes functionality delivered by multiple ClickUp tasks:

* **CU-341** – Fix Android login crash
* **CU-350** – Add login success analytics

Each task is clearly referenced inside the code to maintain traceability.

---

## Example Code (main.py)

```python
"""
Repository: mobile-app
Branch: main

This file represents production-ready code.
All changes merged here come from Pull Requests
linked to ClickUp tasks.
"""

from auth import login_user
from metrics import track_event

"""
Repository: mobile-app
Branch: main

This file represents production-ready code.
All changes merged here come from Pull Requests
linked to ClickUp tasks.
"""

from auth import login_user
from metrics import track_event


def validate_credentials(user_credentials: dict) -> None:
    """
    CU-341: Prevent crashes by validating input before attempting login.
    Raises ValueError for invalid credentials.
    """
    username = (user_credentials.get("username") or "").strip()
    password = (user_credentials.get("password") or "").strip()

    if not username:
        raise ValueError("Username is required.")
    if not password:
        raise ValueError("Password is required.")


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
        # CU-341: Validate before calling login_user to avoid crashes on empty fields
        validate_credentials(user_credentials)

        user = login_user(user_credentials)

        # CU-350: Track successful login event
        track_event(
            event_name="login_success",
            user_id=user["id"]
        )

        print("User logged in successfully.")

    except ValueError as error:
        # CU-350 (extension): Track failed login attempts with reason
        track_event(
            event_name="login_failed",
            user_id=None,
            reason=str(error)
        )
        print(f"Login failed: {error}")

    except Exception as error:
        # Unexpected errors still bubble up after logging
        track_event(
            event_name="login_error",
            user_id=None,
            error_type=type(error).__name__
        )
        print("Unexpected error occurred.")
        raise


if __name__ == "__main__":
    main()


---

## How This Maps to ClickUp

### ClickUp Tasks

Each ClickUp task:

* Is created and tracked in ClickUp
* Is referenced in GitHub branches, commits, and PRs
* Appears in code comments once merged

Example task IDs:

* CU-341
* CU-350

---

### Branches

Work is done in task-specific branches:

```
bugfix/CU-341-login-crash
feature/CU-350-login-analytics
```

These branches are merged into `main` via Pull Requests.

---

### Commits

Each commit references the ClickUp task ID:

```
CU-341 Fix crash when password is empty
CU-350 Add login success tracking
```

This creates a clear audit trail from ClickUp to code.

---

### Pull Requests

Pull Requests:

* Reference ClickUp task IDs in the title
* Trigger CI checks via GitHub Actions
* Must be reviewed before merging

Example PR titles:

```
CU-341 Fix Android login crash
CU-350 Add login success analytics
```

---

## GitHub Actions (Optional)

When configured, GitHub Actions:

* Run tests on Pull Requests
* Block merges if checks fail
* Provide status visibility back in ClickUp

---

## End-to-End Flow

1. Task is created in ClickUp (e.g., CU-341)
2. Engineer creates a task-specific branch
3. Code is written and committed
4. Pull Request is opened
5. CI checks run
6. PR is approved and merged into `main`
7. Task is marked **Done** in ClickUp

---

## Key Takeaway
