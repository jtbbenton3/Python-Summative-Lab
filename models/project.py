from utils import storage
from models.user import User

PROJECTS_FILE = "projects.json"

class Project:
    def __init__(self, id: int, title: str, description: str, due_date: str | None, owner_email: str):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date  # expected format YYYY-MM-DD or None
        self.owner_email = owner_email  # user email (must exist)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "owner_email": self.owner_email,
        }

    @classmethod
    def all(cls) -> list:
        data = storage.load_json(PROJECTS_FILE, [])
        return [cls(**p) for p in data]

    @classmethod
    def create(cls, title: str, description: str, owner_email: str, due_date: str | None = None):
        # ensure owner exists
        owner = next((u for u in User.all() if u.email == owner_email), None)
        if not owner:
            raise ValueError("Owner email not found")

        projects = storage.load_json(PROJECTS_FILE, [])

        # unique title per owner (case-insensitive)
        if any(p["owner_email"] == owner_email and p["title"].lower() == title.lower() for p in projects):
            raise ValueError("Project title already exists for this user")

        new_id = storage.next_id(projects)
        proj = cls(new_id, title, description, due_date, owner_email)
        projects.append(proj.to_dict())
        storage.save_json(PROJECTS_FILE, projects)
        return proj
