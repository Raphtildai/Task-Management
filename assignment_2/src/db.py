import sqlite3

# This class represents a database for managing tasks.
class TaskManagerDB:
    def __init__(self, db_name = 'manager.db'):
        """
        This is a Python constructor function that initializes an object with a specified database name.
        
        :param db_name: The `__init__` method is a special method in Python classes used for
        initializing new objects. In this case, the `__init__` method takes a parameter `db_name`, which
        is the name of a database that the class will interact with. This parameter allows you to
        specify the name of the database you want to connect to
        """
        self.db_name = db_name

    def connect_db(self):
        """
        This function is used to connect to a database.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        return conn, cursor

    def disconnect_db(self, conn, cursor):
        """
        This function is used to disconnect from a database by closing the connection and cursor.
        
        :param conn: The `conn` parameter typically refers to the database connection object that is
        used to connect to a database. It holds the connection information such as the database server
        address, username, password, and other connection settings
        :param cursor: The `cursor` parameter is typically a database cursor object that allows you to
        interact with the database by executing SQL queries and fetching results. It is used to send SQL
        statements to the database and retrieve data from the database result sets
        """
        cursor.close()
        conn.close()
        return {"success": True, "message": "Database connection closed successfully", "data": []}

    def create_task_table(self):
        """
        This function creates a task table.
        """
        conn, cursor = self.connect_db()
        try:
            sql = '''CREATE TABLE IF NOT EXISTS task_manager (
                        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        due_date DATE NOT NULL,
                        status TEXT NOT NULL,
                        description TEXT,
                        flag TEXT NOT NULL,
                        priority TEXT
                    )'''
            cursor.execute(sql)
            conn.commit()
            response = {"success": True, "message": "Task table created successfully", "data": []}
        except sqlite3.Error as e:
            response = {"success": False, "message": f"Error creating task table: {e}", "data": []}
        finally:
            self.disconnect_db(conn, cursor)
        return response

    def create_teams_table(self):
        """
        This function is intended to create a table for storing information about teams.
        """
        conn, cursor = self.connect_db()
        try:
            sql = '''CREATE TABLE IF NOT EXISTS teams (
                        team_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task_id INTEGER,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        FOREIGN KEY(task_id) REFERENCES task_manager(task_id)
                    )'''
            cursor.execute(sql)
            conn.commit()
            response = {"success": True, "message": "Teams table created successfully", "data": []}
        except sqlite3.Error as e:
            response = {"success": False, "message": f"Error creating teams table: {e}", "data": []}
        finally:
            self.disconnect_db(conn, cursor)
        return response

    def save_to_db(self, task_data):
        """
        This function saves task data to a database.
        
        :param task_data: The `save_to_db` method is used to save task data to a database. The
        `task_data` parameter refers to the data related to the task that needs to be saved in
        the database. This data include information such as task title, due date, status, description, 
        flag, team 
        """
        conn, cursor = self.connect_db()
        try:
            # Save task data
            sql_task = '''INSERT INTO task_manager (title, due_date, status, description, flag, priority)
                          VALUES (?, ?, ?, ?, ?, ?)'''
            cursor.execute(sql_task, (task_data['title'], task_data['due_date'], task_data['status'],
                                      task_data['description'], task_data['flag'], task_data['priority']))
            conn.commit()
            
            task_id = cursor.lastrowid  # Get the ID of the newly inserted task

            # If flag is "work", save team data
            if task_data['flag'] == "work" and 'teams' in task_data:
                sql_team = '''INSERT INTO teams (task_id, first_name, last_name) VALUES (?, ?, ?)'''
                for team_name in task_data['teams']:
                    cursor.execute(sql_team, (task_id, team_name.get("first_name"), team_name.get("last_name")))
                conn.commit()

            response = {"success": True, "message": "Data saved successfully", "data": task_data}
        except sqlite3.Error as e:
            response = {"success": False, "message": f"Error saving data: {e}", "data": []}
        finally:
            self.disconnect_db(conn, cursor)
        return response
    
    def fetch_members(self, task_id):
        """
        Fetches members associated with a specific task ID from the database.
        
        :param task_id: The ID of the task for which members are to be retrieved.
        """
        conn, cursor = self.connect_db()
        try:
            sql_teams = '''SELECT * FROM teams WHERE task_id = ?'''
            cursor.execute(sql_teams, (task_id,))
            data = [(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()]
            if len(data) == 0:
                response = {"success": True, "message": f"No Members found", "data": []}
            else:
                response = {"success": True, "message": f"Members found", "data": data}                
            
        except sqlite3.Error as e:
            response = {"success": False, "message": f"Error loading data: {e}", "data": []}
        finally:
            self.disconnect_db(conn, cursor)
        return response
        
    def load_from_db(self):
        """
        This function is used to load data from a database.
        """
        conn, cursor = self.connect_db()
        try:
            # Fetch tasks
            sql_tasks = '''SELECT * FROM task_manager'''
            cursor.execute(sql_tasks)
            tasks = cursor.fetchall()

            # Enrich tasks with teams if the flag is "work"
            enriched_tasks = []
            for task in tasks:
                task_id, title, due_date, status, description, flag, priority = task
                task_dict = {
                    "task_id": task_id,
                    "title": title,
                    "due_date": due_date,
                    "status": status,
                    "description": description,
                    "flag": flag,
                    "priority": priority,
                    "teams": []
                }

                if flag == "work":
                    teams = self.fetch_members(task_id)
                    task_dict["teams"] = teams["data"]

                enriched_tasks.append(task_dict)

            response = {"success": True, "message": "Data loaded successfully", "data": enriched_tasks}
        except sqlite3.Error as e:
            response = {"success": False, "message": f"Error loading data: {e}", "data": []}
        finally:
            self.disconnect_db(conn, cursor)
        return response
    
    def find_single_task(self, task_id):
        """
        This function is used to find a single task based on its task_id.

        :param task_id: The `find_single_task` method is used to search for a specific task based on its
        `task_id`. The `task_id` parameter is the unique identifier of the task that you want to find.
        """
        conn, cursor = self.connect_db()
        response = {}
        try:
            sql = '''SELECT * FROM task_manager WHERE task_id = ?'''
            cursor.execute(sql, (task_id,))
            row = cursor.fetchone()
            if row:
                # Convert row to a dictionary 
                task_data = {
                    "task_id": row[0],
                    "title": row[1],
                    "due_date": row[2],
                    "status": row[3],
                    "description": row[4],
                    "flag": row[5],
                    "priority": row[6],
                }
                if row[5] == "work":
                    members = self.fetch_members(task_id)
                    task_data["teams"] = members["data"] if members["data"] else []

                response = {"success": True, "message": "Task found", "data": task_data}
                return response
            else:
                response = {"success": False, "message": "Task not found", "data": []}
                return response
        except sqlite3.Error as e:
            response = {"success": False, "message": f"Error finding task: {e}", "data": []}
            return response
        finally:
            self.disconnect_db(conn, cursor)

    def insert_team_member(self, task_id, first_name, last_name):
        """
        Inserts a new team member into the database.

        :param task_id: The ID of the task to associate with the team member.
        :param first_name: The first name of the team member.
        :param last_name: The last name of the team member.
        """
        conn, cursor = self.connect_db()
        try:
            sql_insert_team = '''INSERT INTO teams (task_id, first_name, last_name) VALUES (?, ?, ?)'''
            cursor.execute(sql_insert_team, (task_id, first_name, last_name))
            conn.commit()
            return {"success": True, "message": "Team member added successfully"}
        except sqlite3.Error as e:
            return {"success": False, "message": f"Error inserting team member: {e}"}
        finally:
            self.disconnect_db(conn, cursor)


    def update_team_member(self, team_id, task_id, first_name, last_name):
        """
        Updates an existing team member's details in the database.

        :param team_id: The ID of the team member to update.
        :param task_id: The ID of the task to where the member belongs to.
        :param first_name: The updated first name of the team member.
        :param last_name: The updated last name of the team member.
        """
        conn, cursor = self.connect_db()
        try:
            sql_update_team = '''UPDATE teams SET first_name = ?, last_name = ? WHERE team_id = ? AND task_id = ?'''
            cursor.execute(sql_update_team, (first_name, last_name, team_id, task_id))
            conn.commit()
            return {"success": True, "message": "Team member updated successfully"}
        except sqlite3.Error as e:
            return {"success": False, "message": f"Error updating team member: {e}"}
        finally:
            self.disconnect_db(conn, cursor)


    def delete_team_member(self, team_id, task_id):
        """
        Deletes a team member from the database.

        :param team_id: The ID of the team member to delete.
        :param task_id: The ID of the task to where the member belongs to.
        """
        conn, cursor = self.connect_db()
        try:
            sql_delete_team = '''DELETE FROM teams WHERE team_id = ? AND task_id = ?'''
            cursor.execute(sql_delete_team, (team_id, task_id))
            conn.commit()
            return {"success": True, "message": "Team member deleted successfully"}
        except sqlite3.Error as e:
            return {"success": False, "message": f"Error deleting team member: {e}"}
        finally:
            self.disconnect_db(conn, cursor)

    def update_in_db(self, task_id, task_update):
        """
        Updates a task and its associated team members in the database.

        :param task_id: The unique identifier of the task to update.
        :param task_update: A dictionary containing the updated task and team information.
        """
        task = self.find_single_task(task_id)
        if not task["success"]:
            return {"success": False, "message": "Task with the specified ID does not exist", "data": []}

        conn, cursor = self.connect_db()
        try:
            # Update the task details
            sql_task = '''UPDATE task_manager 
                        SET title = ?, due_date = ?, status = ?, description = ?, flag = ?, priority = ?
                        WHERE task_id = ?'''
            cursor.execute(sql_task, (task_update['title'], task_update['due_date'], task_update['status'],
                                    task_update['description'], task_update['flag'], task_update['priority'], task_id))
            conn.commit()

            # Handle team updates if the task is flagged as "work"
            if task_update.get('flag') == "work":
                # Check if 'teams' key exists in the task_update
                if 'teams' not in task_update:
                    # If no teams provided, delete all existing team members for the task
                    teams_members = self.fetch_members(task_id)["data"]
                    if teams_members is not None:
                        for team_id, task_id, first_name, last_name in teams_members:
                            self.delete_team_member(team_id, task_id)
                else:
                    # Process team updates
                    # Fetch existing team members
                    team = self.fetch_members(task_id)["data"]
                    existing_teams = [(row[0], row[1], row[2], row[3]) for row in team] if team else []

                    # Prepare updated team data
                    new_teams = task_update["teams"]

                    # Update or add new members
                    updated_team_ids = []
                    for new_team in new_teams:
                        if isinstance(new_team, tuple):
                            # Unpack the tuple if new_team is a tuple
                            first_name, last_name = new_team[-2:]
                        elif isinstance(new_team, dict):
                            # Safely access if new_team is a dictionary
                            first_name, last_name = new_team.get("first_name"), new_team.get("last_name")
                        else:
                            continue  # Skip invalid entries

                        found = False
                        for team_id, task_id, existing_first, existing_last in existing_teams:
                            name_change = first_name == existing_first and last_name == existing_last
                            if name_change:
                                updated_team_ids.append(team_id)
                                found = True
                                break
                            elif team_id not in updated_team_ids:
                                # Update existing member
                                self.update_team_member(team_id, task_id, first_name, last_name)
                                updated_team_ids.append(team_id)
                                found = True
                                break

                        if not found:
                            # Insert new member
                            self.insert_team_member(task_id, first_name, last_name)

                    # Delete members not in the updated list
                    for team_id, task_id, first_name, last_name in existing_teams:
                        if team_id not in updated_team_ids:
                            self.delete_team_member(team_id, task_id)

            updated_task = self.find_single_task(task_id)
            response = {"success": True, "message": "Task and teams updated successfully", "data": updated_task["data"]}
        except sqlite3.Error as e:
            response = {"success": False, "message": f"Error updating task: {e}", "data": []}
        finally:
            self.disconnect_db(conn, cursor)
        return response

    def delete_from_db(self, task_id):
        """
        Deletes a task from the database. If the task's flag is 'work', it deletes the associated teams first to avoid foreign key violations.
        
        :param task_id: The ID of the task to delete.
        :return: A dictionary containing the status of the deletion.
        """
        task = self.find_single_task(task_id)
        if not task["success"]:
            return {"success": False, "message": "Task with the specified ID does not exist", "data": []}
        else: 
            conn, cursor = self.connect_db()
            try:
                # Check if the flag is 'work'
                flag = task.get("flag") 
                if flag == "work":
                    # Delete associated teams first
                    sql_teams = '''DELETE FROM teams WHERE task_id = ?'''
                    cursor.execute(sql_teams, (task_id,))
                
                # Delete the task
                sql_task = '''DELETE FROM task_manager WHERE task_id = ?'''
                cursor.execute(sql_task, (task_id,))
                conn.commit()
                response = {"success": True, "message": "Task and associated teams deleted successfully", "data": []}
                return response
            except sqlite3.Error as e:
                response = {"success": False, "message": f"Error deleting task: {e}", "data": []}
                return response
            finally:
                self.disconnect_db(conn, cursor)

if __name__ == "__main__":
    # Example usage
    db = TaskManagerDB()

    # Creating tables
    print(db.create_task_table())
    print(db.create_teams_table())

    # # Saving a work task with teams
    # work_task_data = {
    #     "title": "Team Project",
    #     "due_date": "2024/12/12",
    #     "status": "pending",
    #     "description": "Complete the team project",
    #     "flag": "work",
    #     "priority": "low",
    #     "teams": [("Raphael", "Tildai"), ("Dr. Gerel", "Lec")]
    # }
    # print(db.save_to_db(work_task_data))

    # # Saving a personal task
    # personal_task_data = {
    #     "title": "Personal Errand",
    #     "due_date": "2024/12/15",
    #     "status": "pending",
    #     "description": "Buy groceries",
    #     "flag": "personal",
    #     "priority": "low"
    # }
    # print(db.save_to_db(personal_task_data))


    # # Finding a task
    # print(db.find_single_task(1))

    # # Updating a task
    # update_personal_task_data = {
    #     "title": "Updated Report",
    #     "due_date": "2024/12/15",
    #     "status": "pending",
    #     "description": "Final report submitted",
    #     "flag": "work",
    #     "priority": "medium"
    # }
    # print(db.update_in_db(1, update_personal_task_data))
    # # Updating a task
    # update_work_task_data = {
    #     "title": "Team Project",
    #     "due_date": "2024/12/16",
    #     "status": "completed",
    #     "description": "Complete the team project",
    #     "flag": "work",
    #     "priority": "low",
    #     "teams": [("Dr. Gerel", "Lec")]
    # }
    # print(db.update_in_db(2, update_work_task_data))

    # # Loading tasks
    # print(db.load_from_db())

    # # # Deleting a task
    # # print(db.delete_from_db(1))
