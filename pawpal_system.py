"""PawPal+ core classes: Task, Pet, Owner, and Scheduler."""

import datetime
from dataclasses import dataclass, field
import warnings


@dataclass
class Task:
    """A single pet-care task, such as a walk or a feeding."""

    description: str
    time: datetime.time
    frequency: str = "once"  # for example: "once", "daily", "weekly"
    completed: bool = False
    due_date: datetime.date = field(
        default_factory=datetime.date.today
    )

    def mark_complete(self):
        """Mark this task done and return its next daily/weekly occurrence, or None."""
        if self.completed:
            return None

        self.completed = True

        if self.frequency == "daily":
            next_date = self.due_date + datetime.timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.due_date + datetime.timedelta(weeks=1)
        else:
            return None

        return Task(
            description=self.description,
            time=self.time,
            frequency=self.frequency,
            due_date=next_date
        )


@dataclass
class Pet:
    """Stores a pet's details and its list of tasks."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def get_info(self) -> str:
        """Return the pet's information as text."""
        return f"{self.name} ({self.species}, age {self.age})"

    def update_info(self, name=None, species=None, age=None):
        """Update the pet's details. Only the values you pass in are changed."""
        if name is not None:
            self.name = name
        if species is not None:
            self.species = species
        if age is not None:
            self.age = age

    def add_task(self, task: Task):
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Remove a task from this pet."""
        self.tasks.remove(task)

    def get_tasks(self) -> list[Task]:
        """Return all of this pet's tasks."""
        return self.tasks


@dataclass
class Owner:
    """A person who uses PawPal+ to manage their pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet):
        """Remove a pet (and its tasks) from the owner's list."""
        self.pets.remove(pet)

    def view_pets(self) -> list[Pet]:
        """Return all of the owner's pets."""
        return self.pets

    def get_all_tasks(self) -> list[Task]:
        """Collect and return the tasks from every pet."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Organizes an owner's tasks. It gets tasks through owner.get_all_tasks()."""

    def __init__(self, owner: Owner):
        """Create a scheduler that works with the given owner's tasks."""
        self.owner = owner

    def sort_tasks_by_time(self) -> list[Task]:
        """Return all tasks ordered from earliest to latest time of day."""
        return sorted(self.owner.get_all_tasks(), key=lambda task: task.time)

    def get_incomplete_tasks(self) -> list[Task]:
        """Return only the tasks that are not completed yet."""
        return [task for task in self.owner.get_all_tasks() if not task.completed]
    
    def filter_tasks(self, pet_name=None, completed=None) -> list[Task]:
        """Return tasks matching a pet name and/or completion status (None skips a filter)."""
        filtered_tasks = []

        for pet in self.owner.view_pets():
            if pet_name is not None and pet.name.lower() != pet_name.lower():
                continue

            for task in pet.get_tasks():
                if completed is not None and task.completed != completed:
                    continue

                filtered_tasks.append(task)

        return filtered_tasks
    
    def find_pet_for_task(self, task: Task):
        """Return the pet that owns this exact task, or None if no pet has it."""
        for pet in self.owner.view_pets():
            if any(t is task for t in pet.get_tasks()):
                return pet
        return None

    def mark_task_complete(self, pet: Pet, task: Task):
        """Complete a pet's task, add its next occurrence to that pet, and return it (or None)."""
        # "is" checks for the exact same object, not just an equal-looking one
        if not any(t is task for t in pet.get_tasks()):
            raise ValueError("This task does not belong to the selected pet.")

        next_task = task.mark_complete()

        if next_task is None:
            return None

        # Skip it if the pet already has an open task for that same slot
        already_scheduled = any(
            t.description == next_task.description
            and t.time == next_task.time
            and t.due_date == next_task.due_date
            and not t.completed
            for t in pet.get_tasks()
        )
        if already_scheduled:
            return None

        pet.add_task(next_task)
        return next_task

    
    def detect_conflicts(self) -> list[str]:
        """Return warnings for tasks scheduled at the same date and time."""
        warnings = []
        scheduled_times = {}

        for pet in self.owner.view_pets():
            for task in pet.get_tasks():

                # Ignore tasks that are already completed
                if task.completed:
                    continue

                # Identify tasks by date and time
                key = (task.due_date, task.time)

                if key in scheduled_times:
                    other_pet, other_task = scheduled_times[key]

                    warning = (
                        f"WARNING: Scheduling conflict at "
                        f"{task.time.strftime('%I:%M %p')} "
                        f"on {task.due_date}! "
                        f"{other_pet.name}: {other_task.description} "
                        f"and {pet.name}: {task.description}"
                    )

                    warnings.append(warning)

                else:
                    scheduled_times[key] = (pet, task)

        return warnings

