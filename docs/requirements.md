# Project Tracker CLI — Problem Definition

## Purpose
To build a Python-based Command-Line Interface (CLI) application for managing a simulated multi-user project tracker system. This will allow admins to create and manage users, projects, and tasks with persistence.

## Requirements
- Create and manage users, projects, and tasks.
- Assign projects to specific users.
- Assign tasks to projects and mark them complete.
- Search/display projects assigned to specific users.
- Persist data locally using JSON file I/O.
- Use pip to manage external packages (e.g., rich, python-dateutil).
- Structure code with modules, classes, and object relationships.
- Implement one-to-many (User → Projects) and one-to-many (Project → Tasks) relationships.

## CLI Actions (examples)
- `add-user --name "Alex"`
- `add-project --user "Alex" --title "CLI Tool"`
- `add-task --project "CLI Tool" --title "Implement add-task"`

## Deliverables
- Fully functional CLI tool
- External dependencies tracked in Pipfile
- Tests with pytest
- Public GitHub repo with commits, branches, and documentation


