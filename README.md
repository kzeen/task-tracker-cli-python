# Task Tracker CLI - Python

## What it is
Simple CLI project used to track and manage tasks. Tracks what you need to do,
what you have done, and what you are currently working on. Find on [roadmap.sh](https://roadmap.sh/projects/task-tracker).

## Features
- Add, update, delete tasks
- Mark a task as in progress or done
- List all tasks
- List all tasks that are done
- List all tasks that are not done
- List all tasks that are in progress

## How it works
- Runs from the command line
- Accepts user inputs and actions as arguments
- Stores and reads tasks from a JSON file

## How to use it
### Initialization
1. Clone or install the source code to your machine\
`git clone git@github.com:kzeen/task-tracker-cli-python.git`\
Make sure you have *at least* `tracker.py` and `pyproject.toml` in your directory
2. Create a Python virtual environment (Optional but recommended)\
`python -m venv venv`
3. Activate the virtual environment (Run this for every new session)\
`source venv/bin/activate` or `source venv/Scripts/activate` on Windows
4. Create an executable command `tracker` so as not to run `python tracker.py` each time instead\
`python -m pip install -e .`\
Run this only once
5. You can now use the CLI application\
`tracker add 'My task'`

### Documentation
- `tracker add <task_description>`
  - Creates a task with `<task_description>` and an automatically generated ID
  - `<task_description>` must either be one word or enclosed between quotations
- `tracker update <task_id> <new_description>`
  - Updates description of task with ID of `<task_id>` to `<new_description>`
  - `<new_description>` must also be one word or enclosed between quotations
- `tracker delete <task_id>`
  - Deletes task with ID of `<task_id>`
- `tracker mark-in-progress <task_id>`
  - Sets status of task with ID of `<task_id>` to `in-progress`
- `tracker mark-done <task_id>`
  - Sets status of task with ID of `<task_id>` to `done`
- `tracker mark-todo <task_id>`
  - Sets status of task with ID of `<task_id>` to `todo`
- `tracker list [task_status]`
  - If a status is not specified, lists all tasks by order of creation
  - If a status is specified, filters and lists only tasks of that status
  - Possible statuses are `(in-progress, done, todo)`
- You can access this documentation by running `tracker --help`