"""Core logic for the logistics task management system."""
import heapq
from dataclasses import dataclass

PRIORITIES = {"high": 1, "medium": 2, "low": 3}
STATUSES = ("new", "assigned", "complete")


class ValidationError(ValueError):
    """Raised when user input is not valid."""


@dataclass
class Task:
    id: int
    title: str
    driver: str
    priority: str
    due: str  # format HH:MM
    status: str = "new"


def validate_task(title, driver, priority, due):
    if not isinstance(title, str) or not title.strip():
        raise ValidationError("Title is required")
    if len(title) > 80:
        raise ValidationError("Title is too long")
    if not isinstance(driver, str) or not driver.strip():
        raise ValidationError("Driver is required")
    if priority not in PRIORITIES:
        raise ValidationError("Priority must be high, medium or low")
    parts = due.split(":") if isinstance(due, str) else []
    if len(parts) != 2 or not all(p.isdigit() for p in parts):
        raise ValidationError("Due time must look like 14:30")
    if not (0 <= int(parts[0]) <= 23 and 0 <= int(parts[1]) <= 59):
        raise ValidationError("Due time is not a real time")


class TaskManager:
    def __init__(self):
        self._tasks = []  # always kept sorted by id so binary search works
        self._next_id = 1

    def add_task(self, title, driver, priority, due):
        validate_task(title, driver, priority, due)
        task = Task(self._next_id, title.strip(), driver.strip(), priority, due, "assigned")
        self._tasks.append(task)
        self._next_id += 1
        return task

    def all_tasks(self):
        return list(self._tasks)

    def get_by_id(self, task_id):
        """Binary search on the id list."""
        low, high = 0, len(self._tasks) - 1
        while low <= high:
            mid = (low + high) // 2
            current = self._tasks[mid].id
            if current == task_id:
                return self._tasks[mid]
            if current < task_id:
                low = mid + 1
            else:
                high = mid - 1
        return None

    def search_title(self, query):
        q = query.strip().lower()
        return [t for t in self._tasks if q in t.title.lower()]

    def next_task(self, driver):
        """Return the most urgent open task for a driver using a priority queue."""
        heap = []
        for t in self._tasks:
            if t.driver == driver and t.status != "complete":
                heapq.heappush(heap, (PRIORITIES[t.priority], t.due, t.id))
        if not heap:
            return None
        return self.get_by_id(heap[0][2])

    def task_list(self, driver):
        """Open tasks for a driver, most urgent first."""
        open_tasks = [t for t in self._tasks if t.driver == driver and t.status != "complete"]
        return sorted(open_tasks, key=lambda t: (PRIORITIES[t.priority], t.due))

    def complete_task(self, task_id):
        task = self.get_by_id(task_id)
        if task is None:
            raise KeyError("Task not found")
        task.status = "complete"
        return task

    def reassign(self, task_id, new_driver):
        task = self.get_by_id(task_id)
        if task is None:
            raise KeyError("Task not found")
        if not new_driver.strip():
            raise ValidationError("Driver is required")
        task.driver = new_driver.strip()
        return task
