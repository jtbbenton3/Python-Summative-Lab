from __future__ import annotations
from typing import Optional
from utils import storage
from models.user import User
from models.project import Project

TASKS_FILE = "tasks.json"
ALLOWED_STATUS = ["todo", "done"]


class Task:
    def __init__(self, id: int, title: str, status: str, project_id: int, assigned_to: Optional[str] = None):
        self.id = id
        self.title = title
        self.status = status
        self.project_id = project_id
        self.assigned_to = assigned_to

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "project_id": self.project_id,
            "assigned_to": self.assigned_to
        }

    @classmethod
    def all(cls) -> list[Task]:
        tasks_data = storage.load_json(TASKS_FILE, [])
        return [cls(**data) for data in tasks_data]

    @classmethod
    def create(cls, title: str, project_id: int, status: str = "todo", assigned_to: Optional[str] = None) -> Task:
        # validate status
        if status not in ALLOWED_STATUS:
            raise ValueError("Status must be 'todo' or 'done'")

        # ensure project exists
        project = next((p for p in Project.all() if p.id == project_id), None)
        if not project:
            raise ValueError("Project not found")

        # if assigned_to provided, ensure user exists
        if assigned_to:
            if not any(u.email == assigned_to for u in User.all()):
                raise ValueError("Assigned user email not found")

        tasks = storage.load_json(TASKS_FILE, [])

        # unique task title per project (case-insensitive)
        if any(t["project_id"] == project_id and t["title"].lower() == title.lower() for t in tasks):
            raise ValueError("Task title already exists for this project")

        new_id = storage.next_id(tasks)
        task = cls(new_id, title, status, project_id, assigned_to)
        tasks.append(task.to_dict())
        storage.save_json(TASKS_FILE, tasks)
        return task

    @classmethod
    def mark_done(cls, task_id: int) -> Task:
        tasks = storage.load_json(TASKS_FILE, [])
        for t in tasks:
            if t["id"] == task_id:
                t["status"] = "done"
                storage.save_json(TASKS_FILE, tasks)
                return cls(**t)
        raise ValueError("Task not found")