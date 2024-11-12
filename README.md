# Task Manager Application
## By: Kipchirchir Raphael - LGL7CS

## Overview
The Task Manager Application is designed to help users organize and track their personal and work-related tasks efficiently. It allows users to create, view, delete, and save tasks to a CSV file, as well as load previously saved tasks. The application also provides functionality to view pending and overdue tasks based on the current date.

## Key Features
- Task Creation: Create both personal and work-related tasks.
- Task Management: View, delete, and update tasks.
- CSV Integration: Save and load tasks to/from a CSV file.
- Task Status: View tasks by status (pending or overdue).
- User-Friendly Interface: Command-line interface to interact with the application.

## Setup Instructions
To run this application, ensure you have Python 3.12.0 or higher installed. The application requires no external dependencies beyond the standard Python library.

## Steps to Run:
1. Clone or download the repository.

2. Install Python 3.12.0 or higher from the official Python website.
3. Run the program by executing the following command in your terminal:
    ```bash 
    python interface.py
    ```
4. Follow the on-screen instructions to interact with the task manager:
    - # Menu Screen
        ![alt text](image.png)

    - # Creating personal task
        ![alt text](image-1.png)

    - # Creating work task
        ![alt text](image-2.png)

    - # View Tasks
        ![alt text](image-3.png)

    - # Delete a task
        ![alt text](image-4.png)

    - # Save the task list to a CSV file
        ![alt text](image-5.png)

    - # Load tasks from a CSV file
        ![alt text](image-6.png)

    - # View pending and overdue tasks
        ![alt text](image-7.png)

    - # Exit
        ![alt text](image-8.png)

## Class and Method Descriptions
- # TaskManager (in task_manager.py)
    The TaskManager class manages the collection of tasks. It provides methods to add, list, delete, save, and load tasks.

    ## Methods:
    - `__init__(self)`: Initializes the task manager with an empty list of tasks and a default CSV file name.
    - `add_task(self, task)`: Adds a task to the list of tasks.
    - `list_tasks(self, flag=None)`: Lists all tasks, or filters tasks based on a specified class (e.g., 
    
- # PersonalTask or WorkTask).
    - `delete_task(self, task_id)`: Deletes a task by its unique task ID.
    - `save_task(self) `: Saves all tasks to a CSV file.
    - `load_task(self)`: Loads tasks from the CSV file into the task manager.
    - `get_pending_tasks(self)`: Returns all tasks marked as "pending".
    - `get_overdue_tasks(self)`: Returns all tasks that are overdue.

    - # Example Usage:
        ```bash
        task_manager = TaskManager()
        task_manager.add_task(PersonalTask("Finish Homework", "2024/11/10"))
        task_manager.list_tasks()
        task_manager.save_task()
        ```

- # Task (in task.py)
    The Task class is the base class for both personal and work tasks. It defines the properties common to all tasks, such as task ID, title, due date, and status.

    # Methods:
    - `__init__(self, title, due_date)` : Initializes a new task with a title, due date, and a default "pending" status.
    - `mark_completed(self)`: Marks the task as completed.
    - `get_task_id(self)`: Returns the unique task ID.
    - `get_description(self)`: Returns the task description.
    - `set_description(self, desc)`: Sets the task description (up to 15 characters).
    - `__str__(self)`: Returns a string representation of the task, including its ID, title, due date, status, and description.
    - # Example Usage:
        ```bash
        task = Task("Do Laundry", "2024/11/10")
        task.set_description("Wash clothes")
        print(task)
        ```
- # PersonalTask (in task.py)
    The PersonalTask class extends the Task class and adds properties specific to personal tasks, such as priority.

    # Methods:

    - `is_high_priority(self)`: Returns True if the task has a high priority.
    - `set_priority(self, task_priority)`: Sets the task's priority to one of the allowed values: "high", "medium", or "low".
    - `__str__(self)`: Extends the Task class's string representation by adding the priority.
    - # Example Usage:
        ```bash
        personal_task = PersonalTask("Buy Groceries", "2024/11/11")
        personal_task.set_priority("high")
        print(personal_task)
        ```
- # WorkTask (in task.py)
    The WorkTask class extends the Task class and includes functionality specific to work tasks, such as adding team members.

    # Methods:
    - `add_team_member(self, member)`: Adds a team member to the task.
    - `__str__(self)`: Extends the Task class's string representation by adding team members.
    - # Example Usage:
        ```bash
        work_task = WorkTask("Prepare Presentation", "2024/11/20")
        work_task.add_team_member("Dr. Gerel")
        work_task.add_team_member("Raphael")
        print(work_task)
        ```
 - # Error Handling
    - The program provides basic error handling to ensure smooth user interaction.

    - Invalid Input for Task Type: If the user provides an invalid task type when creating a task (e.g., not "personal" or "work"), the program prints an error message:
        ```bash
        print("Invalid task type.")
        ```
    - Description Length Validation: If the description exceeds 15 characters when setting it for a task, a ValueError is raised:
        ```bash
        raise ValueError("Description cannot exceed 15 characters.")
        ```
    - File Not Found: If the CSV file is not found when attempting to load tasks, the program prints a friendly error message:
        ```bash
        print("No saved tasks found.")
        ```
    - Invalid Menu Option: If the user selects an invalid menu option, the program prompts the user to select a valid option.
        ```bash
        print(f"Please enter a valid menu option. Enter a number between 1 and {len(menu_options)}")
        ```
    - Task Not Found: If the user attempts to delete a task with an invalid ID, an error message is displayed:
        ```bash
        print("Task not found.")
        ```

## Future Enhancements
1. Graphical User Interface (GUI): Implement a GUI for users to interact with the application using a more intuitive interface.
2. Recurring Tasks: Add support for recurring tasks (e.g., daily, weekly).
3. Notifications: Implement notifications to remind users of pending or overdue tasks.
4. Database Integration: Consider saving tasks to a database for permanent storage, as an alternative to the CSV file.

## References
1. https://www.geeksforgeeks.org/writing-csv-files-in-python/
2. https://docs.python.org/3/library/csv.html
3. https://realpython.com/python-csv/
4. Lecture and Practice notes and codes 
