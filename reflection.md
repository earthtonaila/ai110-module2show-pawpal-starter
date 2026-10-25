# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
My UML contains the class "Pet" with attibutes name, species, age; along with the methods get_info() and update_info(). This class is responsible for storing, updating, and providing information about the user's pet.

The second class in my UML is "Owner" which contains the attributes name and pets; along with the methods add_pet(), remove_pet(), and view_pets(). This class is responsible for storing information on the owner of the pet(s). The "Pet" class provides information on the pet(s) that belong to each owner.

The third class in my UML is "Walk" which contains the attributes pet, date, time, duration; along with the methoda schedule_walk() and reschedule_walk(). This class is responsible for storing details about a scheduled walk with a specific pet and rescheduling the walk if needed. The "Pet" class provides information on the pet scheduled to walk in the "Walk" class.

The fourth class in my UML is "TaskManager" which contains the attribute tasks; along with the methods add_task(), remove_task(), view_today_tasks(). This class is responsible for keeping track of pet-care tasks, adding or removing new tasks, and displaying scheduled activities for a specific day. The "Pet" class provides information on the pet being scheduled for tasks or activities and are in need of care.

- What classes did you include, and what responsibilities did you assign to each?
1. Pet class
    - Info
        - stores a pet's name, species, & age
        - provides information about the pet
    - Attributes
        - name : the pet's name
        - species : the type of animal
        - age : the pet's age
    - Methods
        - get_info() : displays the pet's information
        - update_info() : updates the pet's details
2. Owner class
    - Info
        - represents someone using PawPal+ to manage their pets
    - Attributes
        - name : the owner's name
        - pets : a list of pets belonging to the owner
    - Methods
        - add_pet() : adds a pet to the owner's list
        - remove_pet() : removes a pet
        - view_pets() : displays all registered pets
3. Walk class
    - Info
        - stores details about a scheduled walk
        - associates the walk with a specific pet
    - Attributes
        - pet : the pet associated with the walk
        - date : the scheduled date
        - time : the scheduled time
        - duration : how long the walk should last
    - Methods
        - schedule_walk() : schedules a walk
        - reschedule_walk() : changes the walk's date or time
4. TaskManager class
    - Info
        - keeps track of pet-care tasks
        - adds or removes new tasks
        - displays today's scheduled activities
    - Attributes
        - tasks : a list of scheduled tasks
    - Methods
        - add_task() : adds a task
        - remove_task() : removes a task
        - view_today_tasks() : displays tasks scheduled for today

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, my design changed during implementation
1. Method Inputs : methods now take the inputs they need
    - Pet.update_info(name, species, age) takes optional values, so users only pass what they want to change
    - Owner.add_pet(pet), TaskManager.add_task(walk), remove_task(walk) take the object to add or remove
    - view_today_tasks(today) takes a date
    - Walk.rescheduule_walk(new_date, new_time) takes the new date and time
= these changes made the program more concise, readible, and efficient as the inputs taken become more specific to whats actually needed by the methods
2. Walk status
    - Walk now has completed: bool = False
    - Added Walk.mark_completed()
= this change allows for the user to flag whether a walk has been completed or not
3. Removes redundancy
    - Walk.schedule_walk() is gone
    - TaskManager.add_task(walk) is now the way to schedule a walk.
    - Added remove_tasks_for_pet()
= this change fixes a design error where users could potentially schedule a walk twice through both the TaskManager and Walk class, and removes tasks for a pet when the pet is removed
4. Returning data
    - view_pets() returns list[Pet]
    - view_today_tasks() returns list[Walk]
    - get_info() returns str
= methods return data instead of printing values
5. Rearrange order of UML diagram
    - moved TaskManager above Owner
= Owner.remove_pet refers to TaskManager

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used Claude's Anthropic AI agent in VS Code to help identify areas of improvement in my initial UML design, translate my improved UML design into Python classes, and implement the main functionality of PawPal+. In addition to Claude, I also used ChatGPT to clarify the instructions given through CodePath for this project and provide step by step directions on how to navigate my chosen IDE.

I found that specifying at the end of my prompt to not make any changes to the code directly or any related file particularly helpful as it allowed me to verify the changess suggested by Claude first before proceeding. I also found that providing additional context and being clear on what I wanted to be particularly helpful when prompting.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
