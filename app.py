import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

# set_page_config must be the first Streamlit command in the script
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Create an Owner only if one doesn't already exist
if "owner" not in st.session_state:
    st.session_state["owner"] = Owner("Alex")

# Retrieve the saved Owner
owner = st.session_state["owner"]

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

Add your pets, schedule care tasks for them, and see everything in time order.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

# ---------- Owner ----------
owner_name = st.text_input("Owner name", value=owner.name)
owner.name = owner_name  # update the existing Owner (no new Owner is created)

# ---------- Add a Pet ----------
st.subheader("Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    age = st.number_input("Age", min_value=0, max_value=40, value=3)

if st.button("Add pet"):
    if pet_name.strip():
        owner.add_pet(Pet(pet_name.strip(), species, int(age)))
        st.success(f"Added {pet_name.strip()}!")
    else:
        st.warning("Please enter a pet name.")

st.write("**My Pets**")
if owner.view_pets():
    for pet in owner.view_pets():
        st.write(pet.get_info())
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ---------- Schedule a Task ----------
st.subheader("Schedule a Task")

if owner.view_pets():
    pet_names = [pet.name for pet in owner.view_pets()]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        chosen_name = st.selectbox("For which pet?", pet_names)
    with col2:
        description = st.text_input("Task description", value="Morning walk")
    with col3:
        task_time = st.time_input("Time")
    with col4:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task"):
        if description.strip():
            # Find the chosen pet in the owner's list and add the task to it
            chosen_pet = owner.view_pets()[pet_names.index(chosen_name)]
            chosen_pet.add_task(Task(description.strip(), task_time, frequency))
            st.success(f"Added '{description.strip()}' for {chosen_name}!")
        else:
            st.warning("Please enter a task description.")
else:
    st.info("Add a pet first, then you can schedule tasks for it.")

st.divider()

# ---------- Schedule ----------
st.subheader("Schedule")

# The Scheduler gets every pet's tasks through owner.get_all_tasks()
scheduler = Scheduler(owner)
only_incomplete = st.checkbox("Show only incomplete tasks")

if only_incomplete:
    tasks = scheduler.get_incomplete_tasks()
else:
    tasks = scheduler.sort_tasks_by_time()

if tasks:
    for i, task in enumerate(tasks):
        col1, col2 = st.columns([4, 1])
        status = "✅" if task.completed else "⬜"
        with col1:
            st.write(
                f"{status} {task.due_date} {task.time.strftime('%H:%M')} - "
                f"{task.description} ({task.frequency})"
            )
        with col2:
            if not task.completed and st.button("Done", key=f"done_{i}"):
                # Completes the task and, if it repeats, adds the next one to the same pet
                task_pet = scheduler.find_pet_for_task(task)
                scheduler.mark_task_complete(task_pet, task)
                st.rerun()
else:
    st.info("No tasks to show yet.")
