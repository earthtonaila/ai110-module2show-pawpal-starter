
from datetime import time
from pawpal_system import Task, Pet


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
