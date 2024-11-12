import csv
from datetime import datetime
from task import Task, PersonalTask, WorkTask

class TaskManager:
    def __init__(self) -> None:
        self.tasks = []
        self.task_list_file_name = "task_list.csv"

    """Function to add task. Receives the task attributes as parameter"""
    def add_task(self, task):
        self.tasks.append(task)
        print("Task added.")

    """Function to list a list of tasks"""
    def list_tasks(self, flag=None):
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
            columns = ["task_id", "title", "due_date", "status", "description"]
            writer = csv.writer(file)
            writer.writerow(columns)
            for task in self.tasks:
                writer.writerow([task.get_task_id(), task.title, task.due_date, task.status, task.get_description()])

    """Function to load the tasks from the CSV file"""
    def load_task(self):
        try:
            with open(self.task_list_file_name, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['description'] is None:
                        task = Task(row['title'], row['due_date'])
                    else:
                        task = Task(row['title'], row['due_date'])
                        task.set_description(row['description'])
                    self.add_task(task)
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
    task1 = PersonalTask("Do Laundry", "2024/11/10")
    task1.set_description("Keep Clean")
    tsk_mgt.add_task(task1)

    task2 = WorkTask("Submit Assignment", "2024/11/15")
    task2.add_team_member("Dr. Gerel")
    task2.add_team_member("Raph")
    tsk_mgt.add_task(task2)

    tsk_mgt.list_tasks()