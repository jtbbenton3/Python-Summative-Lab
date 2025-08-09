from __future__ import annotations
from typing import Optional, List
from utils import storage
from models.user import User

PROJECTS_FILE = "projects.json"


class Project:
    def __init__(self, id: int, title: str, description: str, owner_email: str, due_date: Optional[str] = None):
        self.id = id
        self.title = title
        self.description = description
        self.owner_email = owner_email
        self.due_date = due_date

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "owner_email": self.owner_email,
            "due_date": self.due_date,
        }

    @classmethod
    def all(cls) -> List["Project"]:
        data = storage.load_json(PROJECTS_FILE, [])
        return [cls(**row) for row in data]

    @classmethod
    def create(cls, title: str, description: str, owner_email: str, due_date: Optional[str] = None) -> "Project":
        # owner must exist
        if not any(u.email == owner_email for u in User.all()):
            raise ValueError("Owner email not found")

        projects = storage.load_json(PROJECTS_FILE, [])

        # unique title per owner (case-insensitive)
        if any(p["owner_email"] == owner_email and p["title"].lower() == title.lower() for p in projects):
            raise ValueError("Project title already exists for this owner")

        new_id = storage.next_id(projects)
        project = cls(new_id, title, description, owner_email, due_date)
        projects.append(project.to_dict())
        storage.save_json(PROJECTS_FILE, projects)
        return project