from task_manager import TaskManager, PersonalTask, WorkTask

def switch_menu(option, task_manager):
    if option == 1:  # Creating a new task
        task_type = input("Enter task type (Personal/Work): ").strip().lower()
        title = input("Enter task title: ")
        due_date = input("Enter due date (YYYY/MM/DD): ")
        if task_type == "personal":
            task = PersonalTask(title, due_date)
            desc = input("Enter description (max 15 characters): ")
            task.set_description(desc)
            task_manager.add_task(task)
        elif task_type == "work":
            task = WorkTask(title, due_date)
            while True:
                member = input("Enter team member name (or type 'done' to finish): ")
                if member.lower() == 'done':
                    break
                task.add_team_member(member)
            task_manager.add_task(task)
        else:
            print("Invalid task type.")
    elif option == 2:  # Viewing all tasks
        task_manager.list_tasks()
    elif option == 3:  # Deleting a task
        task_id = int(input("Enter task ID to delete: "))
        task_manager.delete_task(task_id)
    elif option == 4:  # Saving the task list to a CSV file
        task_manager.save_task()
        print("Tasks saved to CSV.")
    elif option == 5:  # Loading tasks from a CSV file
        task_manager.load_task()
        print("Tasks loaded from CSV.")
    elif option == 6:  # View Pending and overdue tasks
        pending_tasks = task_manager.get_pending_tasks()
        print("Pending Tasks:")
        for task in pending_tasks:
            print(task)
        overdue_tasks = task_manager.get_overdue_tasks()
        print("Overdue Tasks:")
        for task in overdue_tasks:
            print(task)

    main_menu(task_manager)

def main_menu(task_manager):
    menu_options = [
        "Create a Task",
        "View all Tasks",
        "Delete a Task",
        "Save the task list to a CSV file",
        "Load tasks from a CSV file",
        "View pending and overdue tasks",
        "Exit"
    ]
    print("##################################################\n")
    print("--- Welcome To Your Task Manager Application---\n")
    for option in range(len(menu_options)):
        print(f"{option + 1}. {menu_options[option]}")
    print("\n##################################################\n")
    user_input = int(input("Select an option to proceed:\n"))

    if user_input > 0 and user_input <= len(menu_options):
        switch_menu(user_input, task_manager)
    else:
        print(f"Please enter a valid menu option. Enter a number between 1 and {len(menu_options)}")
        main_menu(task_manager)

if __name__ == "__main__":
    task_manager = TaskManager()
    main_menu(task_manager)