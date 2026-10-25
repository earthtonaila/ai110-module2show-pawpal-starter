"""PawPal+ class skeletons based on diagrams/uml_draft.mmd.

Only the structure is defined here (attributes and method names).
The business logic has not been implemented yet.
"""

from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class Pet:
    """Stores a pet's basic information."""

    name: str
    species: str
    age: int

    def get_info(self):
        """Return the pet's information."""
        raise NotImplementedError

    def update_info(self):
        """Update the pet's details."""
        raise NotImplementedError


@dataclass
class Walk:
    """A scheduled walk for one specific pet."""

    pet: Pet  # relationship: a Walk belongs to one Pet
    date: date
    time: time
    duration: int  # length of the walk in minutes

    def schedule_walk(self):
        """Schedule this walk."""
        raise NotImplementedError

    def reschedule_walk(self):
        """Change the walk's date or time."""
        raise NotImplementedError


@dataclass
class Owner:
    """A person who uses PawPal+ to manage their pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)  # relationship: one Owner has many Pets

    def add_pet(self):
        """Add a pet to the owner's list."""
        raise NotImplementedError

    def remove_pet(self):
        """Remove a pet from the owner's list."""
        raise NotImplementedError

    def view_pets(self):
        """Display all of the owner's pets."""
        raise NotImplementedError


@dataclass
class TaskManager:
    """Keeps track of pet-care tasks (walks)."""

    tasks: list[Walk] = field(default_factory=list)  # relationship: manages many Walks

    def add_task(self):
        """Add a task."""
        raise NotImplementedError

    def remove_task(self):
        """Remove a task."""
        raise NotImplementedError

    def view_today_tasks(self):
        """Display the tasks scheduled for today."""
        raise NotImplementedError
