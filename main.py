import argparse
from rich.console import Console
from rich.table import Table

from models.user import User
from models.project import Project
from models.task import Task

console = Console()

parser = argparse.ArgumentParser(prog="main.py")
subparsers = parser.add_subparsers(dest="command")

# -------------------- USER COMMANDS --------------------
add_user_parser = subparsers.add_parser("add-user")
add_user_parser.add_argument("--name", required=True)
add_user_parser.add_argument("--email", required=True)

subparsers.add_parser("list-users")

# -------------------- PROJECT COMMANDS --------------------
add_project_parser = subparsers.add_parser("add-project")
add_project_parser.add_argument("--name", required=True)                 # maps to Project.title
add_project_parser.add_argument("--description", required=True)
add_project_parser.add_argument("--owner-email", required=True)
add_project_parser.add_argument("--due-date", required=False)

subparsers.add_parser("list-projects")

# -------------------- TASK COMMANDS --------------------
add_task_parser = subparsers.add_parser("add-task")
add_task_parser.add_argument("--title", required=True)
add_task_parser.add_argument("--project-id", type=int, required=True)
add_task_parser.add_argument("--assigned-to", required=False)
add_task_parser.add_argument("--status", choices=["todo", "done"], default="todo")

subparsers.add_parser("list-tasks")

complete_task_parser = subparsers.add_parser("complete-task")
complete_task_parser.add_argument("--task-id", type=int, required=True)

# -------------------- MAIN --------------------
args = parser.parse_args()

if args.command == "add-user":
    user = User.create(args.name, args.email)
    console.print(f"[green]User added:[/green] {user.name} ({user.email})")

elif args.command == "list-users":
    users = User.all()
    table = Table(title="Users")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Email", style="yellow")
    for u in users:
        table.add_row(str(u.id), u.name, u.email)
    console.print(table)

elif args.command == "add-project":
    project = Project.create(
        title=args.name,                              # <— important: use title
        description=args.description,
        owner_email=args.owner_email,
        due_date=args.due_date,
    )
    console.print(f"[green]Project added:[/green] {project.title}")

elif args.command == "list-projects":
    projects = Project.all()
    table = Table(title="Projects")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Description", style="yellow")
    table.add_column("Owner Email", style="green")
    table.add_column("Due Date", style="blue")
    for p in projects:
        table.add_row(
            str(p.id),
            p.title,
            p.description,
            p.owner_email,
            p.due_date or ""
        )
    console.print(table)

elif args.command == "add-task":
    task = Task.create(
        title=args.title,
        project_id=args.project_id,
        status=args.status,
        assigned_to=args.assigned_to,
    )
    console.print(f"[green]Task added:[/green] {task.title}")

elif args.command == "list-tasks":
    tasks = Task.all()
    table = Table(title="Tasks")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Status", style="yellow")
    table.add_column("Project ID", style="green")
    table.add_column("Assigned To", style="blue")
    for t in tasks:
        table.add_row(str(t.id), t.title, t.status, str(t.project_id), t.assigned_to or "")
    console.print(table)

elif args.command == "complete-task":
    task = Task.mark_done(args.task_id)
    console.print(f"[green]Task marked as done:[/green] {task.title}")