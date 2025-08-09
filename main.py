import argparse
from rich.table import Table
from rich.console import Console
from models.user import User

def add_user(args):
    try:
        user = User.create(name=args.name, email=args.email)
        print(f"User created: id={user.id}, name={user.name}, email={user.email}")
    except ValueError as e:
        print(f"Error: {e}")

def list_users(args):
    users = User.all()
    users = sorted(users, key=lambda u: u.name.lower())
    table = Table(title="Users")
    table.add_column("ID", justify="right")
    table.add_column("Name")
    table.add_column("Email")
    for u in users:
        table.add_row(str(u.id), u.name, u.email)
    Console().print(table)

def add_project(args):
    print(f"[Placeholder] Adding project: title={args.title}, user_email={args.user_email}")

def list_projects(args):
    print("[Placeholder] Listing all projects...")

def add_task(args):
    print(f"[Placeholder] Adding task: title={args.title}, project_id={args.project_id}")

def list_tasks(args):
    print("[Placeholder] Listing all tasks...")

def complete_task(args):
    print(f"[Placeholder] Marking task {args.task_id} as complete")

def main():
    parser = argparse.ArgumentParser(
        description="Project Tracker CLI Tool"
    )
    subparsers = parser.add_subparsers(title="Commands")

    # add-user
    parser_add_user = subparsers.add_parser("add-user", help="Add a new user")
    parser_add_user.add_argument("--name", required=True, help="Name of the user")
    parser_add_user.add_argument("--email", required=True, help="Email of the user")
    parser_add_user.set_defaults(func=add_user)

    # list-users
    parser_list_users = subparsers.add_parser("list-users", help="List all users")
    parser_list_users.set_defaults(func=list_users)

    # add-project
    parser_add_project = subparsers.add_parser("add-project", help="Add a new project")
    parser_add_project.add_argument("--title", required=True, help="Project title")
    parser_add_project.add_argument("--user-email", required=True, help="Email of project owner")
    parser_add_project.set_defaults(func=add_project)

    # list-projects
    parser_list_projects = subparsers.add_parser("list-projects", help="List all projects")
    parser_list_projects.set_defaults(func=list_projects)

    # add-task
    parser_add_task = subparsers.add_parser("add-task", help="Add a new task")
    parser_add_task.add_argument("--title", required=True, help="Task title")
    parser_add_task.add_argument("--project-id", required=True, type=int, help="ID of the project")
    parser_add_task.set_defaults(func=add_task)

    # list-tasks
    parser_list_tasks = subparsers.add_parser("list-tasks", help="List all tasks")
    parser_list_tasks.set_defaults(func=list_tasks)

    # complete-task
    parser_complete_task = subparsers.add_parser("complete-task", help="Mark a task as complete")
    parser_complete_task.add_argument("--task-id", required=True, type=int, help="ID of the task")
    parser_complete_task.set_defaults(func=complete_task)

    args = parser.parse_args()

    # Run the chosen command
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
