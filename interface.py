from task_manager import TaskManager, PersonalTask, WorkTask

"""Function to switch between menus. We pass the menu option and the task manager class"""
def switch_menu(option, task_manager):
    if option == 1:  # Creating a new task
        task_type = input("Enter task type (Personal/Work): ").strip().lower()
        title = input("Enter task title: ")
        due_date = input("Enter due date (YYYY/MM/DD): ")
        
        # Switching between the task type
        if task_type == "personal":
            task = PersonalTask(title, due_date) # We create a personal task object with the title and due_date
            desc = input("Enter description (max 15 characters): ") # Characters should not exceed 15
            task.set_description(desc)
            task_manager.add_task(task) # We proceed to create a new task
        
        elif task_type == "work":
            task = WorkTask(title, due_date)
            while True:
                member = input("Enter team member name (or type 'done' to finish): ")
                if member.lower() == 'done':
                    break
                task.add_team_member(member)
            task_manager.add_task(task)
        else:
            print("Invalid task type.") # We display an error since the task type does not match what we expect
   
    elif option == 2:  # Viewing tasks
        list_tasks_by_type() # Call the function to prompt user to enter the type of task they want to view
        
    elif option == 3:  # Deleting a task
        task_id = int(input("Enter task ID to delete: "))
        task_manager.delete_task(task_id)
        
    elif option == 4:  # Saving the task list to a CSV file
        task_manager.save_task()
        print("Tasks saved to CSV.")
        
    elif option == 5:  # Loading tasks from a CSV file
        task_manager.load_task()
        
    elif option == 6:  # View Pending and overdue tasks
        pending_tasks = task_manager.get_pending_tasks() # Getting pending tasks
        print("================ Pending Tasks ================")
        if(len(pending_tasks) < 1):
            print("No Pending Tasks!")
        else:
            for task in pending_tasks:
                print(task)
                
        overdue_tasks = task_manager.get_overdue_tasks() # Getting overdue tasks
        print("================ Overdue Tasks ================")
        if(len(overdue_tasks) < 1):
            print("No Overdue Tasks!")
        else: 
            for task in overdue_tasks:
                print(task)
    else:
        print("Kosonom Szepen! Viszlat!")
        print("\n##################################################\n")
        exit()

    main_menu(task_manager)
    
"""Function to get the type of tasks to view"""
def list_tasks_by_type():
    task_type_to_view = int(input("Which tasks would you like to view?\nSelect from the following:\n1. Personal Tasks\n2. Work Tasks\n3. All\n"))
    if(task_type_to_view == 1):
        task_manager.list_tasks(PersonalTask)
    elif(task_type_to_view == 2):
        task_manager.list_tasks(WorkTask)
    elif(task_type_to_view == 3):
        task_manager.list_tasks()
    else:
        print("Please select the correct option!\n")
        list_tasks_by_type()

"""Main menu function that displays the menu options to the user and the user have to select an option to proceed"""
def main_menu(task_manager):
    # We define the set of menu options in a list
    menu_options = [
        "Create a Task",
        "View Tasks",
        "Delete a Task",
        "Save the task list to a CSV file",
        "Load tasks from a CSV file",
        "View pending and overdue tasks",
        "Exit"
    ]
    print("##################################################\n")
    print("--- Welcome To Your Task Manager Application ---\n")
    for option in range(len(menu_options)):
        print(f"{option + 1}. {menu_options[option]}")
    print("\n##################################################\n")
    user_input = int(input("Select an option to proceed:\n"))
    print("\n##################################################\n")

    # We check to validate the menu inputted by the user is within the range of the define menu options
    if user_input > 0 and user_input <= len(menu_options):
        switch_menu(user_input, task_manager)
    else:
        print(f"Please enter a valid menu option. Enter a number between 1 and {len(menu_options)}")
        main_menu(task_manager)

if __name__ == "__main__":
    task_manager = TaskManager()
    main_menu(task_manager)