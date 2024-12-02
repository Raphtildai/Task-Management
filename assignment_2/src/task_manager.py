import csv
from datetime import datetime
from task import Task, PersonalTask, WorkTask
from db import TaskManagerDB


class TaskManager:
    def __init__(self, db) -> None:
        self.db = db  # Assign the database instance

    def add_task(self, task_data):
        print(task_data)
        """
        Add a task to the task list. Supports both Task objects and dictionary-based data.
        """
        if isinstance(task_data, dict):
            # Trigger save to db
            return self.save_task(task_data)  
        else:
            return {"success": False, "message": "The input data for task should be an instance of a Task Class", "data": []} 

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
    
    def update_task(self, task_id, updated_data):
        """
        Update a task with new data based on the provided task ID.
        Uses the `update_in_db` method from the `TaskManagerDB` class.
        """
        # Validate the input data structure
        if not isinstance(updated_data, dict):
            return {
                "success": False,
                "message": "Invalid data format. Expected a dictionary.",
            }

        # Ensure the task exists before attempting an update
        existing_task = self.db.find_single_task(task_id)
        if not existing_task["success"]:
            return {
                "success": False,
                "message": f"Task with ID {task_id} not found.",
            }

        # Merge the existing task data with the updated data
        current_data = existing_task
        merged_data = {**current_data, **updated_data}

        # Call the database method to perform the update
        result = self.db.update_in_db(task_id, merged_data)

        # Return the response from the database update operation
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "data": result["data"],
            }
        else:
            return {
                "success": False,
                "message": result["message"],
            }

    def save_task(self, task_data):
        """
        Save a task to the database.
        Handles both Task objects and dictionary-based task data.
        """
        if isinstance(task_data, Task):
            # Convert Task object to dictionary
            task_data = {
                "title": task_data.title,
                "due_date": task_data.due_date,
                "status": getattr(task_data, "status", "pending"),  # Default to "pending" if not provided
                "description": task_data.get_description(),
                "flag": task_data.flag,
                "team_members": getattr(task_data, "team_members", []),
                "priority": getattr(task_data, "priority", "low"),  # Default to "low" if not provided
            }
        elif not isinstance(task_data, dict):
            # If task_data is neither a Task instance nor a dictionary, return an error
            return {"success": False, "message": "Invalid input format. Provide a Task object or a dictionary.", "data": []}

        # Save the task data to the database
        result = self.db.save_to_db(task_data)
        if result["success"]:
            return {"success": True, "message": "Task saved successfully.", "data": result["data"]}
        else:
            return {"success": False, "message": result["message"], "data": []}

        # Save the task data to the database

    def load_task(self):
        """
        Load tasks from the database into the TaskManager.
        """
        rows = self.db.load_from_db()["data"]

        if not rows:
            return []
        else:
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
    
    def find_task(self, task_id):
        """
        Find a specific task.
        """
        task = self.db.find_single_task(task_id)
        return task

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
        return [task for task in tasks if task["status"] == "pending" and datetime.strptime(task["due_date"], '%Y/%m/%d').date() < current_date]


# Example usage
if __name__ == "__main__":
    db = TaskManagerDB()  # Create database instance
    db.create_task_table()
    db.create_teams_table()
    task_manager = TaskManager(db)

    # # Load tasks from the database
    # task_manager.load_task()
    
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
    # response = task_manager.save_task(work_task_data)
    # print(response)
    
    # response = task_manager.delete_task(3)
    # print(response)
    
    
    
    # # Create a personal task
    # task1 = PersonalTask("Do Laundry", "2024/11/10")
    # task1.set_description("Keep Clean")
    # task_manager.add_task(task1)

    # # Create a work task
    # task2 = WorkTask("Submit Assignment", "2024/11/15")
    # task2.add_team_member("Dr. Gerel")
    # task2.add_team_member("Raph")
    # task_manager.add_task(task2)

    # task_manager.list_tasks(PersonalTask)
    # task_manager.save_task()
    
    # # task_manager.delete_task(3)
    # # task_manager.delete_task(2)
    # # task_manager.delete_task(1)
    # # task_manager.list_tasks()