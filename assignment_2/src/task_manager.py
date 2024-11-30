import csv
from datetime import datetime
from task import Task, PersonalTask, WorkTask
from db import TaskManagerDB


class TaskManager:
    def __init__(self, db) -> None:
        self.tasks = []  # Initialize an empty list for tasks
        self.db = db  # Assign the database instance

    def add_task(self, task_data):
        """
        Add a task to the task list. Supports both Task objects and dictionary-based data.
        """
        if isinstance(task_data, dict):
            # Convert dictionary to a Task object
            task = Task(
                title=task_data["title"],
                due_date=task_data["due_date"],
                flag=task_data["flag"]
            )
            task.set_description(task_data.get("description", ""))
        else:
            task = task_data  
        self.tasks.append(task)

    def list_tasks(self, flag=None):
        """
        List tasks, optionally filtered by the task flag (e.g., PersonalTask or WorkTask).
        """
        tasks = self.db.load_from_db()["data"]
        if not tasks:
            print("There are no tasks!")
            return []

        results = []
        for task in tasks:
            if flag is None or task.get("flag") == flag:
                results.append(task)
                print(task)
        print("\n")
        return results

    def delete_task(self, task_id):
        """
        Delete a task by ID from the database.
        """
        return self.db.delete_from_db(task_id)

    def save_task(self):
        """
        Save tasks to the database.
        """
        for task in self.tasks:
            if isinstance(task, Task):
                # Extract task data from the Task object
                task_data = {
                    "title": task.title,
                    "due_date": task.due_date,
                    "status": getattr(task, "status", "pending"),  # Default to "pending" if not provided
                    "description": task.get_description(),
                    "flag": task.flag,
                    "team_members": getattr(task, "team_members", []),
                    "priority": getattr(task, "priority", "low"),  # Default to "low" if not provided
                }
            else:
                task_data = task  

            # Save the task data to the database
            return self.db.save_to_db(task_data)

    def load_task(self):
        """
        Load tasks from the database into the TaskManager.
        """
        rows = self.db.load_from_db()["data"]

        if not rows:
            self.tasks = []
        else:
            self.tasks = []  # Clear existing tasks
            for row in rows:
                # Create the appropriate task object based on the flag
                if row["flag"] == "work":
                    task = WorkTask(row["title"], row["due_date"])
                    members = self.db.fetch_members(row["task_id"])
                    for member in members:
                        task.add_team_member(f"{member[2]} {member[3]}")
                else:
                    task = PersonalTask(row["title"], row["due_date"])

                # Set additional properties
                task.set_description(row.get("description", ""))
                task.set_task_id(row["task_id"])

                # Add to tasks list
                self.add_task(task)

            print("Tasks loaded from the Database.")
        return self.list_tasks()

    def get_pending_tasks(self):
        """
        Get all pending tasks.
        """
        tasks = self.db.load_from_db()["data"]
        return [task for task in tasks if task["status"].strip().lower() == "pending"]

    def get_overdue_tasks(self):
        """
        Get all overdue tasks.
        """
        tasks = self.db.load_from_db()["data"]
        current_date = datetime.now().date()
        return [task for task in tasks if datetime.strptime(task["due_date"], '%Y/%m/%d').date() < current_date]


# Example usage
if __name__ == "__main__":
    db = TaskManagerDB()  # Create database instance
    task_manager = TaskManager(db)

    # Load tasks from the database
    # task_manager.load_task()

    # tasks = tsk_mgt.load_task()
    # print(tasks)
    # exit()
    
    # # Saving a work task with teams
    # work_task_data = {
    #     "title": "Team Project",
    #     "due_date": "2024/12/12",
    #     "status": "ongoing",
    #     "description": "Complete the team project",
    #     "flag": "work",
    #     "priority": "low",
    #     "teams": [("Raphael", "Tildai"), ("Dr. Gerel", "Lec")]
    # }
    # response = tsk_mgt.save_task(work_task_data)
    # print(response)
    
    # response = tsk_mgt.delete_task(3)
    # print(response)
    
    
    
    # # Create a personal task
    # task1 = PersonalTask("Do Laundry", "2024/11/10")
    # task1.set_description("Keep Clean")
    # tsk_mgt.add_task(task1)

    # # Create a work task
    # task2 = WorkTask("Submit Assignment", "2024/11/15")
    # task2.add_team_member("Dr. Gerel")
    # task2.add_team_member("Raph")
    # tsk_mgt.add_task(task2)

    # tsk_mgt.list_tasks(PersonalTask)
    # tsk_mgt.save_task()
    
    # # tsk_mgt.delete_task(3)
    # # tsk_mgt.delete_task(2)
    # # tsk_mgt.delete_task(1)
    # # tsk_mgt.list_tasks()