import csv
from datetime import datetime
from task import Task, PersonalTask, WorkTask

class TaskManager:
    def __init__(self) -> None:
        self.tasks = []
        self.task_list_file_name = "task_list.csv"

    def add_task(self, task):
        self.tasks.append(task)
        print("Task added.")

    def list_tasks(self, flag=None):
        for task in self.tasks:
            if flag is None or isinstance(task, flag):
                print(task)

    def delete_task(self, task_id):
        task_to_delete = next((task for task in self.tasks if task.get_task_id() == task_id), None)
        if task_to_delete:
            self.tasks.remove(task_to_delete)
            print(f"Task {task_id} deleted.")
        else:
            print("Task not found.")

    def save_task(self):
        with open(self.task_list_file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["task_id", "title", "due_date", "status", "description"])
            for task in self.tasks:
                writer.writerow([task.get_task_id(), task.title, task.due_date, task.status, task.get_description()])

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

    def get_pending_tasks(self):
        return list(filter(lambda task: task.status == "pending", self.tasks))

    def get_overdue_tasks(self):
        current_date = datetime.now().date()
        return [task for task in self.tasks if datetime.strptime(task.due_date, '%Y/%m/%d').date() < current_date]

# Example usage
if __name__ == "__main__":
    tsk_mgt = TaskManager()
    task1 = PersonalTask("Buy groceries", "2024/11/10")
    task1.set_description("Buy milk")
    tsk_mgt.add_task(task1)

    task2 = WorkTask("Project report", "2024/10/30")
    task2.add_team_member("Alice")
    tsk_mgt.add_task(task2)

    tsk_mgt.list_tasks()