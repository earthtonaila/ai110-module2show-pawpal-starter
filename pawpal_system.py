"""PawPal+ core classes: Task, Pet, Owner, and Scheduler."""

import datetime
from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet-care task, such as a walk or a feeding."""

    description: str
    time: datetime.time
    frequency: str = "once"  # for example: "once", "daily", "weekly"
    completed: bool = False

    def mark_complete(self):
        """Mark this task as done."""
        self.completed = True


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
        """Return all tasks ordered from earliest to latest time."""
        return sorted(self.owner.get_all_tasks(), key=lambda task: task.time)

    def get_incomplete_tasks(self) -> list[Task]:
        """Return only the tasks that are not completed yet."""
        return [task for task in self.owner.get_all_tasks() if not task.completed]
