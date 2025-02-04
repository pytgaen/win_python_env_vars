import argparse
import sys
from win_env_manager.env_handlers import UserEnvHandler, SystemEnvHandler


def main():
    if not sys.platform.startswith("win"):
        print("Error: This tool requires Windows operating system", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Windows Environment Variables Manager"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--user", action="store_true", help="User-level variables (default)"
    )
    group.add_argument(
        "--system", action="store_true", help="System-level variables (requires admin)"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # List command
    subparsers.add_parser("list", help="List all variables")

    # Get command
    get_parser = subparsers.add_parser("get", help="Get specific variable value")
    get_parser.add_argument("var_name", help="Variable name")
    get_parser.add_argument(
        "--empty",
        action="store_true",
        help="Return empty string if variable doesn't exist",
    )
    get_parser.add_argument(
        "--auto", action="store_true", help="Try user then system variables"
    )

    # Set command
    set_parser = subparsers.add_parser("set", help="Set variable value")
    set_parser.add_argument("var_name", help="Variable name")
    set_parser.add_argument("value", help="Value to set")

    # Unset command
    unset_parser = subparsers.add_parser("unset", help="Delete an environment variable")
    unset_parser.add_argument("var_name", help="Variable name to delete")

    # Add to PATH
    add_parser = subparsers.add_parser("add-to-path", help="Add directory to PATH")
    add_parser.add_argument("directory", help="Directory to add")

    # Remove from PATH
    remove_parser = subparsers.add_parser(
        "remove-from-path", help="Remove directory from PATH"
    )
    remove_parser.add_argument("directory", help="Directory to remove")

    args = parser.parse_args()
    handler = UserEnvHandler() if not args.system else SystemEnvHandler()

    try:
        if args.command == "list":
            for name, value in handler.list_vars().items():
                print(f"{name}={value}")

        elif args.command == "get":
            default = "" if args.empty else None

            if args.auto:
                value = None
                try:
                    value = UserEnvHandler().get_var(args.var_name)
                except FileNotFoundError:
                    value = SystemEnvHandler().get_var(args.var_name, default=default)
            else:
                value = (
                    handler.get_var(args.var_name, default=default)
                    if handler
                    else value
                )
            print(value)

        elif args.command == "set":
            if handler.set_var(args.var_name, args.value):
                print(f"Variable '{args.var_name}' updated successfully")

        elif args.command == "unset":
            if handler.unset_var(args.var_name):
                print(f"Variable '{args.var_name}' deleted")
            else:
                print(f"Variable '{args.var_name}' not found")

        elif args.command == "add-to-path":
            if handler.add_to_path(args.directory):
                print(f"Added '{args.directory}' to PATH")
            else:
                print("Directory already exists in PATH")

        elif args.command == "remove-from-path":
            if handler.remove_from_path(args.directory):
                print(f"Removed '{args.directory}' from PATH")
            else:
                print("Directory not found in PATH")

    except PermissionError:
        print(
            "Error: Administrator privileges required for system variables",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
