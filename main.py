import argparse

from rich.console import Console
from rich.table import Table

from models.user import User
from models.project import Project
from models.task import Task
from storage import load_users, save_users
from utils.helpers import generate_id, validate_date


console = Console()


def find_user(users, username):
    """Find a user by username, ignoring letter case."""
    username = username.strip().lower()

    for user in users:
        if user.username.lower() == username:
            return user

    return None


def find_project(users, project_id):
    """Find a project across all users."""
    for user in users:
        project = user.get_project(project_id)

        if project:
            return project

    return None


def cmd_add_user(args):
    """Create and save a new user."""
    users = load_users()

    if find_user(users, args.username):
        console.print(
            f"[red]User '{args.username}' already exists.[/red]"
        )
        return

    user = User(
        username=args.username.strip(),
        name=args.name.strip(),
        email=args.email.strip(),
    )

    users.append(user)
    save_users(users)

    console.print(
        f"[green]User '{user.username}' created successfully.[/green]"
    )


def cmd_list_users(args):
    """Display all saved users."""
    users = load_users()

    if not users:
        console.print("[yellow]No users found.[/yellow]")
        return

    table = Table(title="Project Manager Users")
    table.add_column("Username")
    table.add_column("Name")
    table.add_column("Email")
    table.add_column("Projects")

    for user in users:
        table.add_row(
            user.username,
            user.name,
            user.email,
            str(len(user.projects)),
        )

    console.print(table)


def cmd_add_project(args):
    """Create a project and assign it to a user."""
    users = load_users()
    user = find_user(users, args.username)

    if not user:
        console.print(
            f"[red]User '{args.username}' was not found.[/red]"
        )
        return

    try:
        due_date = validate_date(args.due_date)
    except (ValueError, TypeError):
        console.print(
            f"[red]Invalid due date: '{args.due_date}'.[/red]"
        )
        return

    project = Project(
        project_id=generate_id(),
        title=args.title.strip(),
        description=args.description.strip(),
        due_date=due_date,
        owner=user.username,
    )

    user.add_project(project)
    save_users(users)

    console.print("[green]Project created successfully.[/green]")
    console.print(f"Project ID: [bold]{project.project_id}[/bold]")
    console.print(f"Title: {project.title}")
    console.print(f"Owner: {project.owner}")
    console.print(f"Due date: {project.due_date or 'Not specified'}")


def cmd_list_projects(args):
    """Display projects for one user or all users."""
    users = load_users()

    if args.username:
        user = find_user(users, args.username)

        if not user:
            console.print(
                f"[red]User '{args.username}' was not found.[/red]"
            )
            return

        selected_users = [user]
        title = f"Projects for {user.username}"
    else:
        selected_users = users
        title = "All Projects"

    table = Table(title=title)
    table.add_column("Project ID")
    table.add_column("Title")
    table.add_column("Owner")
    table.add_column("Due Date")
    table.add_column("Tasks")

    project_count = 0

    for user in selected_users:
        for project in user.projects:
            project_count += 1

            table.add_row(
                project.project_id,
                project.title,
                project.owner,
                str(project.due_date or "Not specified"),
                str(len(project.tasks)),
            )

    if project_count == 0:
        console.print("[yellow]No projects found.[/yellow]")
        return

    console.print(table)


def cmd_add_task(args):
    """Create a task inside an existing project."""
    users = load_users()
    user = find_user(users, args.username)

    if not user:
        console.print(
            f"[red]User '{args.username}' was not found.[/red]"
        )
        return

    project = user.get_project(args.project_id)

    if not project:
        console.print(
            f"[red]Project '{args.project_id}' was not found "
            f"for user '{user.username}'.[/red]"
        )
        return

    contributors = []

    if args.contributors:
        contributors = [
            contributor.strip()
            for contributor in args.contributors.split(",")
            if contributor.strip()
        ]

    task = Task(
        task_id=generate_id(),
        title=args.title.strip(),
        description=args.description.strip(),
        contributors=contributors,
    )

    project.add_task(task)
    save_users(users)

    console.print("[green]Task created successfully.[/green]")
    console.print(f"Task ID: [bold]{task.task_id}[/bold]")
    console.print(f"Title: {task.title}")
    console.print(f"Project: {project.title}")
    console.print(
        f"Contributors: {', '.join(task.contributors) or 'None'}"
    )


def cmd_list_tasks(args):
    """Display all tasks belonging to a project."""
    users = load_users()
    project = find_project(users, args.project_id)

    if not project:
        console.print(
            f"[red]Project '{args.project_id}' was not found.[/red]"
        )
        return

    if not project.tasks:
        console.print(
            f"[yellow]Project '{project.title}' has no tasks.[/yellow]"
        )
        return

    table = Table(title=f"Tasks for {project.title}")
    table.add_column("Task ID")
    table.add_column("Title")
    table.add_column("Status")
    table.add_column("Contributors")

    for task in project.tasks:
        table.add_row(
            task.task_id,
            task.title,
            task.status,
            ", ".join(task.contributors) or "None",
        )

    console.print(table)


def cmd_complete_task(args):
    """Mark an existing task as complete."""
    users = load_users()
    project = find_project(users, args.project_id)

    if not project:
        console.print(
            f"[red]Project '{args.project_id}' was not found.[/red]"
        )
        return

    task_completed = project.complete_task(args.task_id)

    if not task_completed:
        console.print(
            f"[red]Task '{args.task_id}' was not found.[/red]"
        )
        return

    save_users(users)

    console.print(
        f"[green]Task '{args.task_id}' marked as complete.[/green]"
    )


def build_parser():
    """Build and return the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Project Management Command-Line Application",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    add_user_parser = subparsers.add_parser(
        "add-user",
        help="Create a new user",
    )
    add_user_parser.add_argument("--username", required=True)
    add_user_parser.add_argument("--name", required=True)
    add_user_parser.add_argument("--email", required=True)
    add_user_parser.set_defaults(func=cmd_add_user)

    list_users_parser = subparsers.add_parser(
        "list-users",
        help="Display all users",
    )
    list_users_parser.set_defaults(func=cmd_list_users)

    add_project_parser = subparsers.add_parser(
        "add-project",
        help="Create a project for a user",
    )
    add_project_parser.add_argument("--username", required=True)
    add_project_parser.add_argument("--title", required=True)
    add_project_parser.add_argument(
        "--description",
        default="",
    )
    add_project_parser.add_argument(
        "--due-date",
        dest="due_date",
        default=None,
    )
    add_project_parser.set_defaults(func=cmd_add_project)

    list_projects_parser = subparsers.add_parser(
        "list-projects",
        help="Display projects",
    )
    list_projects_parser.add_argument(
        "--username",
        default=None,
        help="Optionally display projects for one user",
    )
    list_projects_parser.set_defaults(func=cmd_list_projects)

    add_task_parser = subparsers.add_parser(
        "add-task",
        help="Create a task inside a project",
    )
    add_task_parser.add_argument(
        "--username",
        required=True,
        help="Username of the project owner",
    )
    add_task_parser.add_argument(
        "--project-id",
        dest="project_id",
        required=True,
    )
    add_task_parser.add_argument("--title", required=True)
    add_task_parser.add_argument(
        "--description",
        default="",
    )
    add_task_parser.add_argument(
        "--contributors",
        default="",
        help="Comma-separated usernames",
    )
    add_task_parser.set_defaults(func=cmd_add_task)

    list_tasks_parser = subparsers.add_parser(
        "list-tasks",
        help="Display tasks belonging to a project",
    )
    list_tasks_parser.add_argument(
        "--project-id",
        dest="project_id",
        required=True,
    )
    list_tasks_parser.set_defaults(func=cmd_list_tasks)

    complete_task_parser = subparsers.add_parser(
        "complete-task",
        help="Mark a task as complete",
    )
    complete_task_parser.add_argument(
        "--project-id",
        dest="project_id",
        required=True,
    )
    complete_task_parser.add_argument(
        "--task-id",
        dest="task_id",
        required=True,
    )
    complete_task_parser.set_defaults(func=cmd_complete_task)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()