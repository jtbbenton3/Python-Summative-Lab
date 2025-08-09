#!/bin/bash
set -e

# 0) Clean slate (keeps the data folder, resets files)
rm -f data/users.json data/projects.json data/tasks.json || true

# 1) Users
python main.py add-user --name "Alex" --email alex@example.com
python main.py add-user --name "Sam"  --email sam@example.com
python main.py list-users

# 2) Projects (owned by different users)
python main.py add-project --title "CLI Tool" --user-email alex@example.com --description "Build the CLI" --due-date 2025-09-01
python main.py add-project --title "Docs"     --user-email sam@example.com  --description "Write docs"   --due-date 2025-09-10
python main.py list-projects

# 3) Tasks (assigned to valid users, on valid projects)
python main.py add-task --title "Implement add-user" --project-id 1 --assigned-to alex@example.com
python main.py add-task --title "Write README"       --project-id 2 --assigned-to sam@example.com
python main.py list-tasks

# 4) Mark a task done & verify
python main.py complete-task --task-id 1
python main.py list-tasks

echo "✅ Smoke test complete."
