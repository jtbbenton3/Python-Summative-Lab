import pytest

from models import user as user_mod
from models import project as project_mod
from models import task as task_mod

def use_tmp_storage(tmp_path):
    user_mod.USERS_FILE = str(tmp_path / "users.json")
    project_mod.PROJECTS_FILE = str(tmp_path / "projects.json")
    task_mod.TASKS_FILE = str(tmp_path / "tasks.json")
    (tmp_path / "users.json").write_text("[]", encoding="utf-8")
    (tmp_path / "projects.json").write_text("[]", encoding="utf-8")
    (tmp_path / "tasks.json").write_text("[]", encoding="utf-8")

def test_user_create_and_list(tmp_path):
    use_tmp_storage(tmp_path)
    u1 = user_mod.User.create("Alex", "alex@example.com")
    u2 = user_mod.User.create("Sam", "sam@example.com")
    all_users = user_mod.User.all()
    assert len(all_users) == 2
    assert all_users[0].email == "alex@example.com"
    assert all_users[1].name == "Sam"
    with pytest.raises(ValueError):
        user_mod.User.create("Alex 2", "alex@example.com")

def test_project_create_requires_owner_and_unique(tmp_path):
    use_tmp_storage(tmp_path)
    owner = user_mod.User.create("Alex", "alex@example.com")
    p1 = project_mod.Project.create(
        title="CLI Tool",
        description="Build the CLI",
        owner_email=owner.email,
        due_date="2025-09-01",
    )
    assert p1.title == "CLI Tool"
    with pytest.raises(ValueError):
        project_mod.Project.create(
            title="CLI Tool",
            description="Another",
            owner_email=owner.email,
            due_date=None,
        )
    with pytest.raises(ValueError):
        project_mod.Project.create(
            title="Docs",
            description="Write docs",
            owner_email="nobody@example.com",
            due_date=None,
        )

def test_task_create_and_complete(tmp_path):
    use_tmp_storage(tmp_path)
    alex = user_mod.User.create("Alex", "alex@example.com")
    proj = project_mod.Project.create(
        title="CLI Tool",
        description="Build the CLI",
        owner_email=alex.email,
        due_date="2025-09-01",
    )
    t1 = task_mod.Task.create(
        title="Set up repo",
        project_id=proj.id,
        status="todo",
        assigned_to=alex.email,
    )
    assert t1.status == "todo"
    assert t1.project_id == proj.id

    done = task_mod.Task.mark_done(t1.id)
    assert done.status == "done"

    tasks = task_mod.Task.all()
    assert len(tasks) == 1
    assert tasks[0].status == "done"

    with pytest.raises(ValueError):
        task_mod.Task.create(
            title="Bad",
            project_id=999,
            status="todo",
            assigned_to=None,
        )