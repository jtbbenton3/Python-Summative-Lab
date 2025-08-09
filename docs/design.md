# Project Tracker CLI — Design

## Classes and Relationships
- **User**
  - Fields: id (int), name (str), email (str)
  - One-to-many: User → Projects

- **Project**
  - Fields: id (int), title (str), description (str), due_date (str, optional)
  - One-to-many: Project → Tasks

- **Task**
  - Fields: id (int), title (str), status (str: 'todo' or 'done'), assigned_to (str, optional)

## IDs
- Integer auto-increment IDs for users, projects, and tasks.

## Persistence
- Separate JSON files: `data/users.json`, `data/projects.json`, `data/tasks.json`

## Validation Rules
- User emails must be unique.
- Project titles must be unique per user.
- Task titles must be unique per project.

## Sorting Defaults
- Users: by name
- Projects: by title
- Tasks: by title

## CLI
- Implemented with `argparse` and subcommands:
  - add-user, list-users
  - add-project, list-projects
  - add-task, list-tasks
  - complete-task
- Arguments validated before processing.

## Output
- Use `rich` to render tables for listing commands.
