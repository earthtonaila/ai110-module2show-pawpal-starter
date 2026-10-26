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

My PawPal+ scheduler primarily considers scheduled time, due date, task completion status, recurrence frequency, and pet assignment.

I prioritized time and scheduling conflicts because they are the most important factors in helping pet owners manage their pets' daily routines. Feeding, walking, and other care activities often need to happen at specific times, so organizing tasks chronologically and identifying conflicts makes the scheduler more useful. 

I also prioritized recurrence because many pet-care responsibilities repeat daily or weekly. I chose these constraints because they directly support the main purpose of PawPal+ while keeping the system simple, readable, and manageable to implement. More advanced features, such as task priorities and user preferences, could be added in the future.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff I made in my PawPal+ scheduling system was prioritizing simplicity and readability over advanced conflict detection.

My detect_conflicts() method uses a dictionary to identify tasks scheduled for the exact same date and time. This approach is efficient because it only needs to examine each task once, and it is easy to understand and debug.

However, this algorithm only detects exact time matches. For example, if one task begins at 9:00 AM and another begins at 9:15 AM, the scheduler will not identify a conflict, even if the tasks overlap in duration.

I chose this simpler approach because my current Task class does not track task durations, and the application is designed as a basic pet-care scheduler. A future improvement would be to add task durations and check for overlapping time intervals.

I also evaluated whether the algorithm could be simplified using more concise Python syntax. I preferred keeping explicit loops and conditions because they make the logic easier to read, explain, and maintain while learning Python.

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

The AI suggested implementing a method named sort_by_time(), but my existing Scheduler class already had a method called sort_tasks_by_time(). So, I didn't accept this modification and instead kept the original name to maintain consistency across my project.

I evaluated AI suggestions by reviewing the generated code, comparing it with my existing class structure, and checking whether it met the assignment requirements.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested task sorting, task filtering, recurring tasks, conflict detection, and task completion. These tests were important because they helped me verify that my scheduler worked correctly and reliably.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I would rate my confidence in my PawPal+ scheduler as 4/5 stars because all my automated tests passed but there's still room for improvement since these pytests don't guarantee that every possible situation has been covered.

If I had additional time, I would test edge cases like a pet with no scheduled tasks, multiple tasks scheduled at the same time, and recurring tasks that cross month or year boundaries.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The part of my PawPal+ project I'm most satisfied with is implementing the smarter scheduling features and integrating them into Streamlit interface.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration of PawPal+, I would focus on improving conflict detection, adding task priorities, and making the user interface more interactive.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that AI is a helpful coding assistant but it is still my resonsibility to make design decisions and verify that the code works correctly