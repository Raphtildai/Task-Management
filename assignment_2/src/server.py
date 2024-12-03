from flask import Flask, jsonify, request
from task_manager import TaskManager
from db import TaskManagerDB

app = Flask(__name__)
db = TaskManagerDB()
task_manager = TaskManager(db)

# Helper function for consistent response formatting
def create_response(message, status, status_code, data=None):
    return {
        "message": message,
        "status": status,
        "status_code": status_code,
        "data": data if data else []
    }

# POST /tasks/new: Add a new task
@app.route('/tasks/new', methods=['POST'])
def create_task():
    data = request.json

    # Validate required fields
    if not data or not all(k in data for k in ("title", "due_date", "flag")):
        response = create_response(
            "Missing required fields: title, due_date, flag.",
            "error",
            400
        )
        return jsonify(response)

    task_data = {
        "title": data.get("title"),
        "due_date": data.get("due_date"),
        "status": data.get("status", "pending"),
        "description": data.get("description", ""),
        "flag": data["flag"],
        "priority": data.get("priority", "low"),
        "teams": data.get("teams", []),
    }

    # Save task
    result = task_manager.add_task(task_data)
    if result["success"]:   
        response = create_response(
            "Task added successfully",
            "success",
            201
        )
        return jsonify(response)
    else:
        response = create_response(
            result["message"],
            "error",
            400
        )
        return jsonify(response)

# GET /tasks/all: Retrieve all tasks
@app.route('/tasks/all', methods=['GET'])
def get_tasks():
    tasks = task_manager.list_tasks()
    message = "Tasks retrieved successfully." if len(tasks) > 0 else "No tasks found."
    response = create_response(
        message,
        "success",
        200,
        tasks
    )
    return jsonify(response)

# GET /tasks/find/<task_id>: Retrieve a task by ID
@app.route('/tasks/find/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    # print("The task ID received is: ",task_id)
    task = task_manager.find_task(task_id)
    return jsonify(task)

# UPDATE /tasks/update<task_id>: update a task by ID
@app.route('/tasks/update/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    # print(f"Request Method: {request.method}")
    # print(f"Request URL: {request.url}")
    # print(f"Request Headers: {request.headers}")
    # print(f"Request Data (raw): {request.data}")
    # print(f"Request JSON: {request.json}")

    data = request.json
    if not data:
        response = create_response(
            "No JSON data provided or invalid JSON format.",
            "error",
            400
        )
        return jsonify(response)

    # Check if the task exists
    task = task_manager.find_task(task_id)
    if not task["success"]:
        return jsonify(task)
    else: 
        # Merge the existing task with the new data
        updated_task = {**task["data"], **data}  # Ensure correct unpacking of task data
        result = task_manager.update_task(task_id, updated_task)  # Save changes
        return jsonify(result)

# DELETE /tasks/delete<task_id>: Delete a task by ID
@app.route('/tasks/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    response_data = task_manager.delete_task(task_id)
    return jsonify(response_data)

# GET /tasks/pending: Retrieve all pending tasks
@app.route('/tasks/pending', methods=['GET'])
def get_pending_tasks():
    tasks = task_manager.get_pending_tasks()
    if not tasks:
        response = create_response(
            "No pending tasks found.",
            "error",
            404
        )
        return jsonify(response)
    response = create_response(
        "Pending tasks retrieved successfully.",
        "success",
        200,
        tasks
    )
    return jsonify(response)

# GET /tasks/overdue: Retrieve all overdue tasks
@app.route('/tasks/overdue', methods=['GET'])
def get_overdue_tasks():
    tasks = task_manager.get_overdue_tasks()
    if not tasks:
        response = create_response(
            "No overdue tasks found.",
            "error",
            404
        )
        return jsonify(response)
    response = create_response(
        "Overdue tasks retrieved successfully.",
        "success",
        200,
        tasks
    )
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
    

# # curl test scripts

# # Creating new task
# # curl -X POST http://127.0.0.1:5000/tasks/new -H "Content-Type: application/json" -d "{\"title\":\"Complete project documentation\",\"due_date\":\"2024/12/15\",\"status\":\"pending\",\"description\":\"Finalize the project documentation for the team.\",\"flag\":\"work\",\"priority\":\"high\",\"teams\":[{\"first_name\":\"John\",\"last_name\":\"Doe\"},{\"first_name\":\"Jane\",\"last_name\":\"Smith\"}]}"

# # Retrieving all tasks
# # curl -X GET http://127.0.0.1:5000/tasks/all

# # Finding a single task
# # curl -X GET http://127.0.0.1:5000/tasks/find/1

# # Updating a task
# # curl -X PUT http://127.0.0.1:5000/tasks/update/1 -H "Content-Type: application/json" -d "{ \"title\": \"Updated Task Title\", \"description\": \"Updated task description\", \"priority\": \"medium\" }"

# # Delete a task
# # curl -X DELETE http://127.0.0.1:5000/tasks/delete/1

# # Retrieve Pending tasks
# # curl -X GET http://127.0.0.1:5000/tasks/pending

# # Retrieve overdue tasks
# # curl -X GET http://127.0.0.1:5000/tasks/overdue
