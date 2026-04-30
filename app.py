from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for demo purposes
tasks = []


@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Task API", "endpoints": ["/tasks", "/tasks/<id>"]})


@app.route("/tasks", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "POST":
        data = request.get_json()
        if not data or "title" not in data:
            return jsonify({"error": "Title is required"}), 400
        
        task = {
            "id": len(tasks) + 1,
            "title": data["title"],
            "completed": data.get("completed", False)
        }
        tasks.append(task)
        return jsonify(task), 201
    
    return jsonify(tasks)


@app.route("/tasks/<int:task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id: int):
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    if request.method == "DELETE":
        tasks.remove(task)
        return jsonify({"message": "Task deleted"})
    
    if request.method == "PUT":
        data = request.get_json()
        task["title"] = data.get("title", task["title"])
        task["completed"] = data.get("completed", task["completed"])
        return jsonify(task)
    
    return jsonify(task)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

