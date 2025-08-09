from utils import storage

USERS_FILE = "users.json"

class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "email": self.email}

    @classmethod
    def all(cls) -> list:
        data = storage.load_json(USERS_FILE, [])
        return [cls(**user) for user in data]

    @classmethod
    def create(cls, name: str, email: str):
        users = storage.load_json(USERS_FILE, [])
        # Validation: unique email
        if any(u["email"] == email for u in users):
            raise ValueError("Email already exists")
        new_id = storage.next_id(users)
        user = cls(new_id, name, email)
        users.append(user.to_dict())
        storage.save_json(USERS_FILE, users)
        return user
