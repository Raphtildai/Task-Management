import csv
from datetime import datetime
from task import Task, PersonalTask, WorkTask


""" Super Class (Task Manager) for managing collection of Task objects"""
class TaskManager:
    def __init__(self) -> None:
        self.tasks = [] # Initializing empty list
        self.task_list_file_name = "task_list.csv"

    """Function to add task. Receives the task attributes as a parameter"""
    def add_task(self, task):
        self.tasks.append(task)

    """Function to list a list of tasks"""
    def list_tasks(self, flag=None):
        if(len(self.tasks) < 1):
            print("There are no tasks!")
        else:
            for task in self.tasks:
                if flag is None or isinstance(task, flag):
                    print(task)
                print("\n")

    """Function to delete a certain task by specifying its ID"""
    def delete_task(self, task_id):
        # Here I used next function (similar to using a for loop) to iterate over the tasks to find what we are looking for by its ID
        task_to_delete = next((task for task in self.tasks if task.get_task_id() == task_id), None)
        if task_to_delete:
            self.tasks.remove(task_to_delete)
            print(f"Task {task_id} deleted.")
        else:
            print("Task not found.")

    """Function to save task to a CSV file"""
    def save_task(self):
        with open(self.task_list_file_name, mode='w', newline='') as file:
            columns = ["task_id", "title", "due_date", "status", "description", "flag", 'team']
            writer = csv.writer(file)
            writer.writerow(columns)

            for task in self.tasks:
                # Prepare the common fields
                task_data = [
                    task.get_task_id(), 
                    task.title, 
                    task.due_date, 
                    task.status, 
                    task.get_description(), 
                    task.flag
                ]
                
                # Add team_members or None based on the flag
                if task.flag == 'personal':
                    task_data.append(None)
                else:
                    task_data.append(task.team_members)
                
                # Write the row
                writer.writerow(task_data)

    """Function to load the tasks from the CSV file"""
    def load_task(self):
        try:
            with open(self.task_list_file_name, mode='r') as file:
                reader = csv.DictReader(file)
                # Convert the reader to a list to check its length
                rows = list(reader)
                
                if len(rows) < 1:
                    self.tasks = []
                else:
                    self.tasks = [] # We set the tasks list to [] since we will display the tasks from the CSV file only
                    for row in rows:
                        if row['description'] is None:
                            task = Task(row['title'], row['due_date'], row['flag'])
                        else:
                            task = Task(row['title'], row['due_date'], row['flag'])
                            task.set_description(row['description'])
                        self.add_task(task)
                    
                    print("Tasks loaded from CSV.")
                return self.list_tasks()
        except FileNotFoundError:
            print("No saved tasks found.")

    """Function to get the pending tasks"""
    def get_pending_tasks(self):
        return list(filter(lambda task: task.status == "pending", self.tasks))

    """Function to get the overdue tasks"""
    def get_overdue_tasks(self):
        current_date = datetime.now().date()
        return [task for task in self.tasks if datetime.strptime(task.due_date, '%Y/%m/%d').date() < current_date]

# Example usage
if __name__ == "__main__":
    tsk_mgt = TaskManager()
    # Create a personal task
    task1 = PersonalTask("Do Laundry", "2024/11/10")
    task1.set_description("Keep Clean")
    tsk_mgt.add_task(task1)

    # Create a work task
    task2 = WorkTask("Submit Assignment", "2024/11/15")
    task2.add_team_member("Dr. Gerel")
    task2.add_team_member("Raph")
    tsk_mgt.add_task(task2)

    tsk_mgt.list_tasks(PersonalTask)
    
    # tsk_mgt.delete_task(3)
    # tsk_mgt.delete_task(2)
    # tsk_mgt.delete_task(1)
    # tsk_mgt.list_tasks()