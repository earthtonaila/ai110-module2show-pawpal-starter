# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```
=== Today's Schedule ===
07:30 AM - Feed Luna
08:00 AM - Feed Buddy
09:30 AM - Walk Buddy
========================

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_tasks_by_time() | The scheduler uses Python's sorted() function with a lambda expression to organize tasks chronologically based on their scheduled time. This ensures that earlier activities appear before later ones, regardless of the order in which the tasks were added. |
| Filtering | Scheduler.filter_tasks() | The scheduler allows users to filter tasks by pet name, completion status, or both. For example, users can retrieve all tasks belonging to Buddy or display only incomplete tasks. The filtering algorithm loops through the owner's pets and collect tasks matching the selected criteria |
| Conflict handling | Scheduler.detect_conflicts() | scheduler detects if multiple incomplete tasks have same due date and scheduled time. uses dictionary to track occupied scheduling slots. when another task is found at an occupied slot, the method generates a warning message instead of crashing the program. The algorithm only checks exact date-and-time matches and doesn't detect overlapping tasks with different start times because task durations are not currently tracked. |
| Recurring tasks | Task.mark_complete(), Scheduler.mark_task_complete() | one-time tasks don't repeat, daily tasks repeat after one day, weekly tasks repeat after seven days |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

## Implementation Summary

PawPal+ is a Python-based pet-care management application that helps owners organize and track activities for multiple pets.

The application uses four main classes:
    1. Task: represents an individual pet-care activity, including its description, scheduled time, frequency, and completion status
    2. Pet: stores information about a pet and manages its assigned tasks
    3. Owner: manages multiple pets and combines their tasks using the get_all_tasks() method
    4. Scheduler: retrieves tasks through the Owner class, sorts them by time, and identifies incomplete activities

These classes work together to provide a centralized schedule for all pets. Each pet stores its own tasks, the owner combines those tasks, and the scheduler organizes them into readable schedule

The application includes a command-line demo in main.py and automated tests using pytest to verify task completion and task addition