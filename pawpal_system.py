"""PawPal+ class skeletons based on diagrams/uml_draft.mmd.

Only the structure is defined here (attributes, method names, and inputs).
The business logic has not been implemented yet.
"""

from dataclasses import dataclass, field
import datetime


@dataclass
class Pet:
    """Stores a pet's basic information."""

    name: str
    species: str
    age: int

    def get_info(self) -> str:
        """Return the pet's information as text."""
        raise NotImplementedError

    def update_info(self, name=None, species=None, age=None):
        """Update the pet's details. Only the values you pass in are changed."""
        raise NotImplementedError


@dataclass
class Walk:
    """A scheduled walk for one specific pet."""

    pet: Pet  # relationship: a Walk belongs to one Pet
    date: datetime.date
    time: datetime.time
    duration: int  # length of the walk in minutes
    completed: bool = False  # becomes True once the walk is done

    def reschedule_walk(self, new_date: datetime.date, new_time: datetime.time):
        """Change the walk's date and time."""
        raise NotImplementedError

    def mark_completed(self):
        """Mark this walk as done."""
        raise NotImplementedError


@dataclass
class TaskManager:
    """Keeps track of pet-care tasks (walks)."""

    tasks: list[Walk] = field(default_factory=list)  # relationship: manages many Walks

    def add_task(self, walk: Walk):
        """Add a walk to the task list (this is how a walk gets scheduled)."""
        raise NotImplementedError

    def remove_task(self, walk: Walk):
        """Remove a single walk from the task list."""
        raise NotImplementedError

    def get_tasks_for_pet(self, pet: Pet) -> list[Walk]:
        """Return all walks that belong to the given pet."""
        raise NotImplementedError

    def remove_tasks_for_pet(self, pet: Pet):
        """Remove every walk that belongs to the given pet."""
        raise NotImplementedError

    def view_today_tasks(self, today: datetime.date) -> list[Walk]:
        """Return the walks scheduled for the given day."""
        raise NotImplementedError


@dataclass
class Owner:
    """A person who uses PawPal+ to manage their pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)  # relationship: one Owner has many Pets

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's list."""
        raise NotImplementedError

    def remove_pet(self, pet: Pet, task_manager: TaskManager):
        """Remove a pet from the owner's list and remove its walks from the task manager."""
        raise NotImplementedError

    def view_pets(self) -> list[Pet]:
        """Return all of the owner's pets."""
        raise NotImplementedError
