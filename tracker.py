import sys
import json
import datetime


ACCEPTED_COMMANDS = ('add', 'update', 'delete', 'mark-in-progress', 'mark-done', 'mark-todo', 'list', '-h', '--help', '-v', '--version')


def get_current_time() -> str:
    """Return the current timestamp"""
    return datetime.datetime.now().isoformat(timespec="seconds")

def validate_args() -> None:
    """Run initial validation of command line arguments, pointing to --help command on errors"""
    if len(sys.argv) <= 1 or sys.argv[1] not in ACCEPTED_COMMANDS:
        help_command()
    else:
        parse_args()

def parse_args() -> None:
    """
    Parse command line arguments according to passed commands.
    Invalid commands/options call --help command.
    """
    match sys.argv[1:]:
        case ['add', task_description]:
            add_task(task_description)
        case ['update', task_id, new_description]:
            update_task(int(task_id), new_description)
        case ['delete', task_id]:
            delete_task(int(task_id))
        case ['mark-in-progress', task_id]:
            update_task_status(int(task_id), "in-progress")
        case ['mark-done', task_id]:
            update_task_status(int(task_id), "done")
        case ['mark-todo', task_id]:
            update_task_status(int(task_id), "todo")
        case ['list']:
            list_tasks()
        case ['list', task_filter]:
            if task_filter in ('done', 'todo', 'in-progress'):
                list_tasks(task_filter)
            else:
                help_command()
        case ['-h' | '--help']:
            help_command()
        case ['-v' | '--version']:
            version_command()
        case _:
            help_command()

def load_tasks() -> list[dict]:
    """
    Read tasks.json and return a list of task dicts.
    Any problem -> return []
    """
    try:
        with open('tasks.json', 'r') as fh:
            tasks = json.load(fh)
            return tasks if isinstance(tasks, list) else []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []

def save_tasks(task_list: list[dict]) -> None:
    """
    Args:
        task_list: List of objects representing tasks
    Takes list of tasks to save to JSON file
    """
    with open('tasks.json', 'w') as fh:
        json.dump(task_list, fh, indent=1)

def add_task(task_description: str) ->  None:
    """
    Args:
        task_description: Description/Title of the task to add
    Adds task to a JSON file for storing
    Creates "tasks.json" if not found
    """
    current_tasks = load_tasks()
    if current_tasks:
        next_id = current_tasks[-1]["id"] + 1
    else:
        next_id = 1

    new_task = {
        "id": next_id,
        "desc": task_description,
        "status": "todo",
        "created_at": get_current_time(),
        "updated_at": get_current_time()
    }
    current_tasks.append(new_task)

    save_tasks(current_tasks)

    print(f"Added task '{task_description}' with ID {next_id}")

def update_task(task_id: int, new_description: str) -> None:
    """
    Args:
        task_id: ID of the task to update
        new_description: New description to update old one
    Searches for specified task
    If found, updates description and 'updated_at'
    If not, nothing happens
    """
    current_tasks = load_tasks()

    if current_tasks:
        task_index = get_task_index(task_id)
        if task_index >= 0:
            current_tasks[task_index]["desc"] = new_description
            current_tasks[task_index]["updated_at"] = get_current_time()

            save_tasks(current_tasks)

            print(f"Updated task ID {task_id} to '{new_description}'")
            return
    # No tasks at all, or ID not found
    print(f"Task with ID {task_id} was not found")

def delete_task(task_id: int) -> None:
    """
    Args:
        task_id: ID of the task to delete
    Searches for the task to delete by ID.
    If found, deletes it from list and updates file
    If not, nothing happens
    """
    current_tasks = load_tasks()

    if current_tasks:
        task_index = get_task_index(task_id)
        if task_index >= 0:
            current_tasks.pop(task_index)

            save_tasks(current_tasks)

            print(f"Deleted task with ID {task_id}")
            return
    # No tasks at all, or ID not found
    print(f"Task with ID {task_id} was not found")

def update_task_status(task_id: int, new_status: str) -> None:
    """
    Args:
        task_id: ID of task to update status of
        new_status: Status to update task to
    Searches for specified task
    If found, updates status and 'updated_at' (if status different from current)
    If not, nothing happens
    """
    current_tasks = load_tasks()

    if current_tasks:
        task_index = get_task_index(task_id)
        if task_index >=0:
            if current_tasks[task_index]["status"] != new_status:
                current_tasks[task_index]["status"] = new_status
                current_tasks[task_index]["updated_at"] = get_current_time()

                save_tasks(current_tasks)

                print(f"Marked task with ID {task_id} as {new_status}")
            else:
                print("Status remained unchanged")
            return
    # No tasks at all, or ID not found
    print(f"Task with ID {task_id} was not found")

def list_tasks(task_filter: str = "") -> None:
    """
    Args:
        task_filter: Optional status filter to show tasks from
    Lists all tasks in order if no filter is provided
    Otherwise, lists tasks under a certain status
    """
    current_tasks = load_tasks()

    if current_tasks:
        filtered_tasks = [task for task in current_tasks if not task_filter or task["status"] == task_filter]

        if filtered_tasks:
            for task in filtered_tasks:
                print(f"ID: {task['id']} - {task['status']}")
                print(f" {task['desc']}\n")
        else:
            print("No tasks with this status exist")
    else:
        print("No tasks to display")

def get_task_index(task_id: int) -> int:
    """
    Args:
        task_id: ID of task to search for
    Searches tasks for matching ID and returns its index if found,
    -1 if not found
    """
    current_tasks = load_tasks()
    if current_tasks:
        for task_index, task in enumerate(current_tasks):
            if task["id"] == task_id:
                return task_index
    return -1

def help_command() -> None:
    """
    Print out the help command on how to use this CLI application
    """
    print("\nTask Tracker\n")
    print("Usage:")
    print("  tracker add <description>")
    print("  tracker update <id> <new_description>")
    print("  tracker delete <id>")
    print("  tracker mark-in-progress <id>")
    print("  tracker mark-done <id>")
    print("  tracker mark-todo <id>")
    print("  tracker list [in-progress | done | todo]")
    print("\n Make sure <description> and <new_description> are between quotations\n")

    print("Options:")
    print("  -h, --help\tPrint out this help message")
    print("  -v, --version\tPrint out version number")

def version_command() -> None:
    """
    Print out the version of this CLI application
    """
    print("\nTask Tracker version 1.0.0\n")

def main() -> None:
    validate_args()


if __name__ == "__main__":
    main()