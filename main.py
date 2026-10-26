
from datetime import date, time
from pawpal_system import Task, Pet, Owner, Scheduler


def main():
    # ========================================
    # 1. CREATE OWNER AND PETS
    # ========================================

    owner = Owner("Alex")

    buddy = Pet("Buddy", "Dog", 3)
    luna = Pet("Luna", "Cat", 2)

    owner.add_pet(buddy)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)

    # ========================================
    # 2. CREATE TASKS OUT OF ORDER
    # ========================================

    walk_buddy = Task(
        "Walk Buddy",
        time(9, 30),
        "daily",
        due_date=date(2026, 10, 25)
    )

    feed_buddy = Task(
        "Feed Buddy",
        time(8, 0),
        "daily",
        due_date=date(2026, 10, 25)
    )

    groom_buddy = Task(
        "Groom Buddy",
        time(14, 0),
        "weekly",
        due_date=date(2026, 10, 25)
    )

    feed_luna = Task(
        "Feed Luna",
        time(7, 30),
        "daily",
        due_date=date(2026, 10, 25)
    )

    # Add tasks in an unsorted order
    buddy.add_task(groom_buddy)
    buddy.add_task(walk_buddy)
    buddy.add_task(feed_buddy)

    luna.add_task(feed_luna)

    # ========================================
    # 3. TEST SORTING
    # ========================================

    print("\n=== ALL TASKS SORTED BY TIME ===")

    for task in scheduler.sort_tasks_by_time():
        formatted_time = task.time.strftime("%I:%M %p")
        print(f"{formatted_time} - {task.description}")

    # ========================================
    # 4. TEST FILTERING
    # ========================================

    print("\n=== BUDDY'S TASKS ===")

    for task in scheduler.filter_tasks(pet_name="Buddy"):
        print(task.description)

    print("\n=== INCOMPLETE TASKS ===")

    for task in scheduler.filter_tasks(completed=False):
        print(task.description)

    # ========================================
    # 5. TEST RECURRING TASKS
    # ========================================

    print("\n=== RECURRING TASK TEST ===")

    print("Original task:", walk_buddy.description)
    print("Original due date:", walk_buddy.due_date)

    next_task = scheduler.mark_task_complete(
        buddy,
        walk_buddy
    )

    print("Original completed:", walk_buddy.completed)

    if next_task:
        print("New task:", next_task.description)
        print("New due date:", next_task.due_date)
        print("New task completed:", next_task.completed)

    # ========================================
    # 6. TEST CONFLICT DETECTION
    # ========================================

    conflict_task1 = Task(
        "Walk Buddy",
        time(9, 0),
        "daily",
        due_date=date(2026, 10, 26)
    )

    conflict_task2 = Task(
        "Feed Luna",
        time(9, 0),
        "daily",
        due_date=date(2026, 10, 26)
    )

    buddy.add_task(conflict_task1)
    luna.add_task(conflict_task2)

    print("\n=== SCHEDULING CONFLICTS ===")

    warnings = scheduler.detect_conflicts()

    if warnings:
        for warning in warnings:
            print(warning)
    else:
        print("No scheduling conflicts found.")

    # ========================================
    # 7. DISPLAY FINAL TASK LIST
    # ========================================

    print("\n=== FINAL TASK LIST ===")

    for pet in owner.view_pets():
        print(f"\nPet: {pet.name}")

        for task in pet.get_tasks():
            print(
                f"{task.due_date} "
                f"{task.time.strftime('%I:%M %p')} - "
                f"{task.description} "
                f"(Completed: {task.completed})"
            )


if __name__ == "__main__":
    main()
