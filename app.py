"""Small web layer so the task manager can be deployed and integrated."""
from flask import Flask, jsonify, request
from tasks import TaskManager, ValidationError

app = Flask(__name__)
manager = TaskManager()
manager.add_task("Deliver parcels to Soweto", "Thabo", "medium", "10:00")
manager.add_task("Collect pallets Smith Street", "Thabo", "high", "09:00")


def as_dict(t):
    return {"id": t.id, "title": t.title, "driver": t.driver,
            "priority": t.priority, "due": t.due, "status": t.status}


@app.get("/")
def home():
    return "<h1>Logistics Task Manager</h1><p>Try /health or /drivers/Thabo/tasks</p>"


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/drivers/<name>/tasks")
def driver_tasks(name):
    return jsonify([as_dict(t) for t in manager.task_list(name)])


@app.post("/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    try:
        t = manager.add_task(data.get("title"), data.get("driver"),
                             data.get("priority"), data.get("due"))
    except ValidationError as err:
        return jsonify(error=str(err)), 400
    return jsonify(as_dict(t)), 201


@app.post("/tasks/<int:task_id>/complete")
def complete(task_id):
    try:
        return jsonify(as_dict(manager.complete_task(task_id)))
    except KeyError:
        return jsonify(error="Task not found"), 404


if __name__ == "__main__":
    app.run()
