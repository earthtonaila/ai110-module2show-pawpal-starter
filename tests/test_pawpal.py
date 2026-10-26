
from datetime import date, time, timedelta

import pytest

from pawpal_system import Task, Pet, Owner, Scheduler


def test_task_completion():
    # Create a task
    task = Task("Walk Buddy", time(9, 0), "daily")

    # Verify the task starts incomplete
    assert task.completed is False

    # Mark the task as complete
    task.mark_complete()

    # Verify the task is now complete
    assert task.completed is True


def test_task_addition():
    # Create a pet
    pet = Pet("Buddy", "Dog", 3)

    # Create a task
    task = Task("Feed Buddy", time(8, 0), "daily")

    # Count the pet's tasks before adding
    initial_count = len(pet.tasks)

    # Add the task to the pet
    pet.add_task(task)

    # Verify the task count increased by one
    assert len(pet.tasks) == initial_count + 1


def make_scheduler(*pets):
    """Helper: build an owner with the given pets and return a Scheduler."""
    owner = Owner("Alex")
    for pet in pets:
        owner.add_pet(pet)
    return Scheduler(owner)


def test_daily_task_creates_next_day_task():
    buddy = Pet("Buddy", "Dog", 3)
    task = Task("Feed Buddy", time(8, 0), "daily", due_date=date(2026, 10, 25))
    buddy.add_task(task)
    scheduler = make_scheduler(buddy)

    next_task = scheduler.mark_task_complete(buddy, task)

    assert next_task.due_date == date(2026, 10, 26)
    assert next_task.completed is False
    assert next_task.description == "Feed Buddy"
    assert next_task.time == time(8, 0)
    assert next_task.frequency == "daily"
    assert len(buddy.tasks) == 2


def test_daily_task_rolls_over_month_end():
    buddy = Pet("Buddy", "Dog", 3)
    task = Task("Feed Buddy", time(8, 0), "daily", due_date=date(2026, 1, 31))
    buddy.add_task(task)

    next_task = make_scheduler(buddy).mark_task_complete(buddy, task)

    assert next_task.due_date == date(2026, 2, 1)


def test_weekly_task_creates_task_seven_days_later():
    buddy = Pet("Buddy", "Dog", 3)
    task = Task("Groom Buddy", time(14, 0), "weekly", due_date=date(2026, 10, 25))
    buddy.add_task(task)

    next_task = make_scheduler(buddy).mark_task_complete(buddy, task)

    assert next_task.due_date == date(2026, 11, 1)
    assert next_task.frequency == "weekly"


def test_one_time_task_does_not_repeat():
    buddy = Pet("Buddy", "Dog", 3)
    task = Task("Vet visit", time(10, 0), "once", due_date=date(2026, 10, 25))
    buddy.add_task(task)

    next_task = make_scheduler(buddy).mark_task_complete(buddy, task)

    assert next_task is None
    assert task.completed is True
    assert len(buddy.tasks) == 1


def test_original_task_stays_completed():
    buddy = Pet("Buddy", "Dog", 3)
    task = Task("Feed Buddy", time(8, 0), "daily", due_date=date(2026, 10, 25))
    buddy.add_task(task)

    make_scheduler(buddy).mark_task_complete(buddy, task)

    assert task.completed is True
    assert task in buddy.tasks
    assert task.due_date == date(2026, 10, 25)


def test_completing_twice_does_not_create_duplicate():
    buddy = Pet("Buddy", "Dog", 3)
    task = Task("Feed Buddy", time(8, 0), "daily", due_date=date(2026, 10, 25))
    buddy.add_task(task)
    scheduler = make_scheduler(buddy)

    first = scheduler.mark_task_complete(buddy, task)
    second = scheduler.mark_task_complete(buddy, task)

    assert first is not None
    assert second is None
    assert len(buddy.tasks) == 2  # the original plus exactly one new task


def test_identical_open_task_blocks_duplicate_occurrence():
    buddy = Pet("Buddy", "Dog", 3)
    today_task = Task("Feed Buddy", time(8, 0), "daily", due_date=date(2026, 10, 25))
    tomorrow_task = Task("Feed Buddy", time(8, 0), "daily", due_date=date(2026, 10, 26))
    buddy.add_task(today_task)
    buddy.add_task(tomorrow_task)

    next_task = make_scheduler(buddy).mark_task_complete(buddy, today_task)

    assert next_task is None
    assert len(buddy.tasks) == 2


def test_next_occurrence_goes_to_the_correct_pet():
    buddy = Pet("Buddy", "Dog", 3)
    luna = Pet("Luna", "Cat", 2)
    buddy_task = Task("Feed", time(8, 0), "daily", due_date=date(2026, 10, 25))
    luna_task = Task("Feed", time(8, 0), "daily", due_date=date(2026, 10, 25))
    buddy.add_task(buddy_task)
    luna.add_task(luna_task)
    scheduler = make_scheduler(buddy, luna)

    # Find Luna's task through the scheduler, then complete it
    pet = scheduler.find_pet_for_task(luna_task)
    assert pet is luna
    scheduler.mark_task_complete(pet, luna_task)

    assert len(luna.tasks) == 2
    assert len(buddy.tasks) == 1


def test_task_must_belong_to_the_given_pet():
    buddy = Pet("Buddy", "Dog", 3)
    luna = Pet("Luna", "Cat", 2)
    # Same values, but two separate task objects
    buddy_task = Task("Feed", time(8, 0), "daily", due_date=date(2026, 10, 25))
    luna_task = Task("Feed", time(8, 0), "daily", due_date=date(2026, 10, 25))
    buddy.add_task(buddy_task)
    luna.add_task(luna_task)

    with pytest.raises(ValueError):
        make_scheduler(buddy, luna).mark_task_complete(buddy, luna_task)


def test_sorting_and_filtering_still_work_with_recurring_tasks():
    buddy = Pet("Buddy", "Dog", 3)
    late = Task("Walk", time(18, 0), "daily", due_date=date(2026, 10, 25))
    early = Task("Feed", time(8, 0), "once", due_date=date(2026, 10, 25))
    buddy.add_task(late)
    buddy.add_task(early)
    scheduler = make_scheduler(buddy)

    scheduler.mark_task_complete(buddy, late)

    assert [t.description for t in scheduler.sort_tasks_by_time()] == ["Feed", "Walk", "Walk"]
    assert len(scheduler.filter_tasks(pet_name="buddy", completed=False)) == 2
    assert len(scheduler.get_incomplete_tasks()) == 2

def test_sorting_correctness():
    """Verify tasks are sorted from earliest to latest."""

    owner = Owner("Alex")
    buddy = Pet("Buddy", "Dog", 3)
    owner.add_pet(buddy)

    # Add tasks out of order
    task1 = Task("Walk", time(14, 0))
    task2 = Task("Feed", time(8, 0))
    task3 = Task("Play", time(11, 0))

    buddy.add_task(task1)
    buddy.add_task(task2)
    buddy.add_task(task3)

    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_tasks_by_time()

    assert sorted_tasks == [task2, task3, task1]


def test_daily_task_recurrence():
    """Verify completing a daily task creates tomorrow's task."""

    owner = Owner("Alex")
    buddy = Pet("Buddy", "Dog", 3)
    owner.add_pet(buddy)

    today = date(2026, 10, 25)

    daily_task = Task(
        "Walk Buddy",
        time(9, 0),
        "daily",
        due_date=today
    )

    buddy.add_task(daily_task)

    scheduler = Scheduler(owner)

    next_task = scheduler.mark_task_complete(buddy, daily_task)

    # Original task is completed
    assert daily_task.completed is True

    # A new task was created
    assert next_task is not None

    # The new task is due the following day
    assert next_task.due_date == today + timedelta(days=1)

    # The new task starts incomplete
    assert next_task.completed is False

    # The new task belongs to Buddy
    assert next_task in buddy.get_tasks()


def test_conflict_detection():
    """Verify tasks at the same date and time cause a warning."""

    owner = Owner("Alex")

    buddy = Pet("Buddy", "Dog", 3)
    luna = Pet("Luna", "Cat", 2)

    owner.add_pet(buddy)
    owner.add_pet(luna)

    # Two tasks scheduled at the same time
    task1 = Task(
        "Walk Buddy",
        time(9, 0),
        "daily",
        due_date=date(2026, 10, 26)
    )

    task2 = Task(
        "Feed Luna",
        time(9, 0),
        "daily",
        due_date=date(2026, 10, 26)
    )

    buddy.add_task(task1)
    luna.add_task(task2)

    scheduler = Scheduler(owner)

    warnings = scheduler.detect_conflicts()

    # At least one conflict should be detected
    assert len(warnings) > 0

    # The warning should mention the conflicting tasks
    assert "Walk Buddy" in warnings[0]
    assert "Feed Luna" in warnings[0]

# Initial code to add a pet in app.py :
# if st.button("Add Buddy"):
#   buddy = Pet("Buddy", "Dog", 3)
#   owner.add_pet(buddy)
