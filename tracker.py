import sys
import json
import datetime


ACCEPTED_COMMANDS = ('add', 'update', 'delete', 'mark-in-progress', 'mark-done', 'list')


def get_current_time() -> str:
    """Return the current timestamp"""
    return datetime.datetime.now().isoformat(timespec="seconds")

def validate_args() -> None:
    """Run initial validation of command line arguments, pointing to --help command on errors"""
    if len(sys.argv) <= 1 or sys.argv[1] not in ACCEPTED_COMMANDS:
        # Show help/usage command
        print("Run --help")
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
        case ['update', task_id, task_description]:
            print("Updated task", task_description, "ID:", task_id)
        case ['delete', task_id]:
            print("Deleted task with ID", task_id)
        case ['mark-in-progress', task_id]:
            print("Marked task with ID", task_id, "as in progress")
        case ['mark-done', task_id]:
            print("Marked task with ID", task_id, "as done")
        case ['list']:
            print("Listing all tasks")
        case ['list', task_filter]:
            if task_filter in ('done', 'todo', 'in-progress'):
                print("Listing tasks marked as", task_filter)
            else:
                print("Run --help")
        case _:
            print("Run --help")

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

    with open('tasks.json', 'w') as fh:
        json.dump(current_tasks, fh, indent=1)

    print(f"Added task '{task_description}' with ID {next_id}")

def main() -> None:
    validate_args()


if __name__ == "__main__":
    main()