from datetime import datetime

class Task:
    _task_counter = 1  # Class variable for auto-incremented task ID

    def __init__(self, title, due_date):
        self._task_id = Task._task_counter  # Unique task ID
        Task._task_counter += 1
        self.title = title
        self.due_date = due_date
        self.status = "pending"
        self._description = None  # Protected attribute

    def mark_completed(self):
        self.status = "completed"

    def get_task_id(self):
        return self._task_id

    def get_description(self):
        return self._description

    def set_description(self, desc):
        if len(desc) > 15:
            raise ValueError("Description cannot exceed 15 characters.")
        self._description = desc

    def __str__(self) -> str:
        return (f"Task description:\n"
                f"Task ID: {self.get_task_id()}\n"
                f"Title: {self.title}\n"
                f"Due date: {self.due_date}\n"
                f"Status: {self.status}\n"
                f"Description: {self.get_description()}")

class PersonalTask(Task):
    def __init__(self, title, due_date):
        super().__init__(title, due_date)
        self.priority = "low"

    def is_high_priority(self):
        return self.priority == "high"

    def set_priority(self, task_priority):
        allowed_priorities = ["high", "medium", "low"]
        if task_priority not in allowed_priorities:
            print(f"Invalid Priority given. The allowed priorities are:\n {allowed_priorities}")
            return
        
        self.priority = task_priority

    def __str__(self) -> str:
        return (super().__str__() + 
                f"\nPriority: {self.priority}")

class WorkTask(Task):
    def __init__(self, title, due_date):
        super().__init__(title, due_date)
        self.team_members = []

    def add_team_member(self, member):
        if member:
            self.team_members.append(member)
        else:
            print("Please enter a valid team member name")

    def __str__(self) -> str:
        team_members_str = ""
        for i in range(len(self.team_members)):
            team_members_str += f"{i + 1}. {self.team_members[i]}\n"
        return (super().__str__() + 
                f"\nTeam Members:\n{team_members_str}")