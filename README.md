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
        print(f"Login failed: {error}")

    except Exception as error:
        print("Unexpected error occurred.")
        raise error


if __name__ == "__main__":
    main()
```

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
