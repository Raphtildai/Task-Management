from flask import Flask, jsonify, request, abort
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

# POST /tasks: Add a new task
@app.route('/tasks', methods=['POST'])
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
    task_manager.add_task(task_data)
    task_manager.save_task()

    response = create_response(
        "Task added successfully",
        "success",
        201
    )
    return jsonify(response)

# GET /tasks: Retrieve all tasks
@app.route('/tasks', methods=['GET'])
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

# GET /tasks/<task_id>: Retrieve a task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    tasks = task_manager.db.load_from_db()["data"]
    task = next((t for t in tasks if t["task_id"] == task_id), None)
    if not task:
        response = create_response(
            "Task not found.",
            "error",
            404
        )
        return jsonify(response)
    response = create_response(
        "Task retrieved successfully.",
        "success",
        200,
        task
    )
    return jsonify(response)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json

    # Validate request data
    if not data:
        response = create_response(
            "No data provided for update.",
            "error",
            400
        )
        return jsonify(response)

    # Check if the task exists
    tasks = task_manager.db.load_from_db()["data"]
    task = next((t for t in tasks if t["task_id"] == task_id), None)
    if not task:
        response = create_response(
            "Task not found.",
            "error",
            404
        )
        return jsonify(response)

    # Update the task
    updated_task = {**task, **data}  # Merge the existing task with the new data
    task_manager.update_task(task_id, updated_task)  # Save changes
    task_manager.save_task()  # Persist to the database

    response = create_response(
        "Task updated successfully.",
        "success",
        200,
        updated_task
    )
    return jsonify(response)

# DELETE /tasks/<task_id>: Delete a task by ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    response_data = task_manager.delete_task(task_id)
    if response_data["success"]:
        response = create_response(
            "Task deleted successfully.",
            "success",
            200
        )
    else:
        response = create_response(
            response_data["message"],
            "error",
            404
        )
    return jsonify(response)

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
