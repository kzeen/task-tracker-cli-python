import sys


ACCEPTED_COMMANDS = ('add', 'update', 'delete', 'mark-in-progress', 'mark-done', 'list')


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
            print("Added", task_description)
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


def main() -> None:
    validate_args()


if __name__ == "__main__":
    main()