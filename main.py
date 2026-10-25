
from datetime import time
from pawpal_system import Task, Pet, Owner, Scheduler


def main():
    # Create an owner
    owner = Owner("Alex")

    # Create two pets
    buddy = Pet("Buddy", "Dog", 3)
    luna = Pet("Luna", "Cat", 2)

    # Add the pets to the owner
    owner.add_pet(buddy)
    owner.add_pet(luna)

    # Create three tasks with different times
    task1 = Task("Feed Buddy", time(8, 0), "daily")
    task2 = Task("Walk Buddy", time(9, 30), "daily")
    task3 = Task("Feed Luna", time(7, 30), "daily")

    # Assign tasks to the pets
    buddy.add_task(task1)
    buddy.add_task(task2)
    luna.add_task(task3)

    # Create a scheduler for the owner
    scheduler = Scheduler(owner)

    # Display today's schedule
    print("=== Today's Schedule ===")

    for task in scheduler.sort_tasks_by_time():
        formatted_time = task.time.strftime("%I:%M %p")
        print(f"{formatted_time} - {task.description}")

    print("========================")


if __name__ == "__main__":
    main()
