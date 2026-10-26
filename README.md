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

## ✨ Features

- **Owner, pets, and tasks:** one `Owner` holds many `Pet` objects, and each `Pet` holds its own list of `Task` objects (description, time of day, frequency, due date, and completion status).
- **Sorting by time:** `Scheduler.sort_tasks_by_time()` lists every pet's tasks from earliest to latest time of day.
- **Filtering:** `Scheduler.filter_tasks()` narrows tasks by pet name (case-insensitive), completion status, or both. `Scheduler.get_incomplete_tasks()` returns only the open tasks.
- **Recurring tasks:** completing a `daily` task creates a new task due one day later, and a `weekly` task creates one due seven days later. `once` tasks do not repeat. The original task stays marked complete, and the new task is added to the same pet.
- **Duplicate protection:** completing the same task twice does not create a second copy, and a next occurrence is skipped if that pet already has an identical open task for that date and time.
- **Conflict detection:** `Scheduler.detect_conflicts()` returns warning messages when two incomplete tasks share the same date and time, including tasks for different pets. It returns messages instead of raising errors.
- **Streamlit interface:** forms for adding pets and tasks, a sorted schedule with "Done" buttons, filters, and conflict warnings. The same `Owner` is kept in `st.session_state`, so it survives Streamlit reruns.
- **Command-line demo:** `main.py` walks through sorting, filtering, recurrence, and conflict detection and prints the results.
- **Automated tests:** 15 pytest tests cover task completion, adding tasks, sorting, recurrence, duplicate completion, and conflict detection.

**Current limitations**

- Tasks have no priority or duration, so there is no daily plan generator and conflicts are exact-match only (overlapping times are not detected).
- Sorting looks at time of day only, not the due date.
- Frequency names are case-sensitive: `"daily"` and `"weekly"` repeat, and anything else is treated as a one-time task.
- Tasks added in the Streamlit app are given today's date as their due date.

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
python -m pytest

# Run with coverage:
pytest --cov
```
The automated tests verify the following behaviors:
    1. Task Sorting - confirms that tasks are sorted in chronological order
    2. Recurring Tasks - verifies that completing a daily task creates a new incomplete task scheduled for the following day
    3. Conflict Detection - checks that the scheduler identifies tasks scheduled at the same date and time
    4. Task Completion - confirms that completed tasks are correctly marked as finished
    5. Task Management - verifies that tasks can be added to a pet's task list

Sample test output:

```
============================== test session starts ===============================
platform darwin -- Python 3.12.6, pytest-9.1.1, pluggy-1.7.0
rootdir: /Users/nailasurahmat/Desktop/Code/ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 15 items                                                               

tests/test_pawpal.py ...............                                       [100%]

=============================== 15 passed in 0.02s ===============================
```
Confidence Level : 4/5 stars
Based on the automated test results, I am confident that PawPal+'s core scheduling features work as intended. The tests help verify that tasks are sorted correctly, recurring tasks are generated, and scheduling conflicts are detected. However, there's still room for improvement. For example, the current conflict detection algorithm checks for tasks scheduled at exactly the same date and time but does not detect overlapping tasks with different start times. Additional edge-case testing and more advanced scheduling features would help improve the system's reliability.

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_tasks_by_time() | The scheduler uses Python's sorted() function with a lambda expression to organize tasks chronologically based on their scheduled time. This ensures that earlier activities appear before later ones, regardless of the order in which the tasks were added. |
| Filtering | Scheduler.filter_tasks() | The scheduler allows users to filter tasks by pet name, completion status, or both. For example, users can retrieve all tasks belonging to Buddy or display only incomplete tasks. The filtering algorithm loops through the owner's pets and collect tasks matching the selected criteria |
| Conflict handling | Scheduler.detect_conflicts() | scheduler detects if multiple incomplete tasks have same due date and scheduled time. uses dictionary to track occupied scheduling slots. when another task is found at an occupied slot, the method generates a warning message instead of crashing the program. The algorithm only checks exact date-and-time matches and doesn't detect overlapping tasks with different start times because task durations are not currently tracked. |
| Recurring tasks | Task.mark_complete(), Scheduler.mark_task_complete() | one-time tasks don't repeat, daily tasks repeat after one day, weekly tasks repeat after seven days |

## 📸 Demo Walkthrough

### The interface

Start the app with `streamlit run app.py`. The page is laid out top to bottom:

1. **Owner name:** renames the one `Owner` stored in `st.session_state`. No new owner is created on rerun.
2. **Add a Pet:** name, species, and age, plus an **Add pet** button. Pets appear under **My Pets**.
3. **Schedule a Task:** choose a pet, then enter a description, time, and frequency (`once`, `daily`, or `weekly`) and click **Add task**. This section appears once you have at least one pet.
4. **Schedule:** every task with a ✅ or ⬜ status, its due date, time, and frequency. A **Done** button completes a task, and a checkbox shows only incomplete tasks.
5. **Smart Scheduling Dashboard:**
   - **Upcoming Tasks:** a table of all tasks sorted by time, with a Pet column.
   - **Filter Tasks:** dropdowns for pet and status (All, Incomplete, Completed) that feed `Scheduler.filter_tasks()`.
   - **Scheduling Conflicts:** one `st.warning()` per conflict, or `st.success()` when there are none.

### Example workflow

1. Add two pets, **Buddy** (dog) and **Luna** (cat).
2. Schedule a **daily** "Walk" for Buddy at 09:00, then a **once** "Feed" for Luna at 09:00. Both are due today.
3. The Scheduling Conflicts section now shows a warning naming both tasks, because they share the same date and time.
4. Click **Done** on Luna's one-time "Feed". She has no next task, and the conflict warning is replaced by the success message.
5. Click **Done** on Buddy's daily "Walk". It stays in the list as completed, and a new pending "Walk" due tomorrow is added to Buddy.
6. In **Filter Tasks**, choose Buddy and Incomplete to see only his open tasks.

### How the Scheduler works

- **Sorting:** `sorted(owner.get_all_tasks(), key=lambda task: task.time)`. Python compares each task's `datetime.time`. Tasks at the same time keep the order they were added, and the due date is ignored.
- **Filtering:** loop over the owner's pets, skip any pet whose name does not match (ignoring case), then loop over its tasks and skip any whose `completed` value does not match. Passing `None` for a filter skips it.
- **Recurring tasks:** `mark_task_complete(pet, task)` first checks that the task belongs to that pet, then calls `task.mark_complete()`. That marks the task done and returns a copy dated with `timedelta` (1 day for daily, 7 days for weekly), or `None` for a one-time task or a task that was already complete. The copy is skipped if the pet already has an open task with the same description, time, and date. Otherwise it is added to the pet.
- **Conflict detection:** loop over every incomplete task and use `(due_date, time)` as a dictionary key. The first task at a key is stored. Each later task at the same key produces a warning string naming both pets and tasks. With three or more tasks in one slot, each later task is compared with the first.

### Output from `main.py`

Running `python main.py` prints this (the demo uses fixed dates in October 2026):

```
=== ALL TASKS SORTED BY TIME ===
07:30 AM - Feed Luna
08:00 AM - Feed Buddy
09:30 AM - Walk Buddy
02:00 PM - Groom Buddy

=== BUDDY'S TASKS ===
Groom Buddy
Walk Buddy
Feed Buddy

=== INCOMPLETE TASKS ===
Groom Buddy
Walk Buddy
Feed Buddy
Feed Luna

=== RECURRING TASK TEST ===
Original task: Walk Buddy
Original due date: 2026-10-25
Original completed: True
New task: Walk Buddy
New due date: 2026-10-26
New task completed: False

=== SCHEDULING CONFLICTS ===
WARNING: Scheduling conflict at 09:00 AM on 2026-10-26! Buddy: Walk Buddy and Luna: Feed Luna

=== FINAL TASK LIST ===

Pet: Buddy
2026-10-25 02:00 PM - Groom Buddy (Completed: False)
2026-10-25 09:30 AM - Walk Buddy (Completed: True)
2026-10-25 08:00 AM - Feed Buddy (Completed: False)
2026-10-26 09:30 AM - Walk Buddy (Completed: False)
2026-10-26 09:00 AM - Walk Buddy (Completed: False)

Pet: Luna
2026-10-25 07:30 AM - Feed Luna (Completed: False)
2026-10-26 09:00 AM - Feed Luna (Completed: False)
```

What each part shows:

- **Sorted by time:** tasks from both pets appear in time order even though they were added out of order.
- **Filtering:** Buddy's three tasks, then all four incomplete tasks.
- **Recurring task:** completing the daily "Walk Buddy" due 2026-10-25 leaves the original completed and creates a new incomplete one due 2026-10-26 at 09:30 AM.
- **Conflict:** two tasks at 09:00 AM on 2026-10-26 (one per pet) produce one warning.
- **Final task list:** the recurring task's new copy sits in Buddy's list next to the original.

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