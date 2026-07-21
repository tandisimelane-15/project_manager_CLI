import argparse
import sys

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

def cmd_edit_task(args):
    """Edit a task's title and/or description."""
    users = load_users()
    project = find_project(users, args.project_id)

    if not project:
        console.print(
            f"[red]Project '{args.project_id}' was not found.[/red]"
        )
        return

    task = project.get_task(args.task_id)

    if not task:
        console.print(
            f"[red]Task '{args.task_id}' was not found.[/red]"
        )
        return

    if args.title is None and args.description is None:
        console.print("[yellow]No changes were supplied.[/yellow]")
        return

    task.edit(
        title=args.title,
        description=args.description,
    )

    save_users(users)

    console.print(
        f"[green]Task '{task.title}' updated successfully.[/green]"
    )

def cmd_delete_task(args):
    """Delete a task from a project."""
    users = load_users()
    project = find_project(users, args.project_id)

    if not project:
        console.print(
            f"[red]Project '{args.project_id}' was not found.[/red]"
        )
        return

    task = project.get_task(args.task_id)

    if not task:
        console.print(
            f"[red]Task '{args.task_id}' was not found.[/red]"
        )
        return

    project.tasks.remove(task)
    save_users(users)

    console.print(
        f"[green]Task '{task.title}' deleted successfully.[/green]"
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

    edit_task_parser = subparsers.add_parser(
    "edit-task",
    help="Edit a task",
)

    edit_task_parser.add_argument(
        "--project-id",
        dest="project_id",
        required=True,
    )

    edit_task_parser.add_argument(
        "--task-id",
        dest="task_id",
        required=True,
    )

    edit_task_parser.add_argument(
        "--title",
    )

    edit_task_parser.add_argument(
        "--description",
    )

    edit_task_parser.set_defaults(func=cmd_edit_task)

    delete_task_parser = subparsers.add_parser(
    "delete-task",
    help="Delete a task",
    )

    delete_task_parser.add_argument(
        "--project-id",
        dest="project_id",
        required=True,
        help="ID of the project containing the task",
    )

    delete_task_parser.add_argument(
        "--task-id",
        dest="task_id",
        required=True,
        help="ID of the task to delete",
    )

    delete_task_parser.set_defaults(func=cmd_delete_task)

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


def prompt_required(message):
    """Prompt until the user enters a non-empty value."""
    while True:
        value = input(message).strip()
        if value:
            return value
        console.print("[red]This field cannot be blank.[/red]")


def select_user(users):
    """Display users as a numbered list and return the selected user."""
    if not users:
        console.print("[yellow]No users are available. Please create a user first.[/yellow]")
        return None

    console.print("\n[bold]Available Users[/bold]")
    for number, user in enumerate(users, start=1):
        console.print(f"{number}. {user.name} ([cyan]{user.username}[/cyan])")

    while True:
        selection = input("Select a user number, or press Enter to cancel: ").strip()
        if selection == "":
            return None
        try:
            index = int(selection) - 1
            if 0 <= index < len(users):
                return users[index]
        except ValueError:
            pass
        console.print("[red]Please enter a valid user number.[/red]")


def select_project(projects):
    """Display projects as a numbered list and return the selected project."""
    if not projects:
        console.print("[yellow]No projects are available.[/yellow]")
        return None

    console.print("\n[bold]Available Projects[/bold]")
    for number, project in enumerate(projects, start=1):
        due_date = project.due_date or "No due date"
        console.print(
            f"{number}. {project.title} "
            f"([cyan]{project.owner}[/cyan]) — {due_date}"
        )

    while True:
        selection = input("Select a project number, or press Enter to cancel: ").strip()
        if selection == "":
            return None
        try:
            index = int(selection) - 1
            if 0 <= index < len(projects):
                return projects[index]
        except ValueError:
            pass
        console.print("[red]Please enter a valid project number.[/red]")


def select_task(tasks):
    """Display tasks as a numbered list and return the selected task."""
    if not tasks:
        console.print("[yellow]No tasks are available.[/yellow]")
        return None

    console.print("\n[bold]Available Tasks[/bold]")
    for number, task in enumerate(tasks, start=1):
        console.print(f"{number}. {task.title} — [cyan]{task.status}[/cyan]")

    while True:
        selection = input("Select a task number, or press Enter to cancel: ").strip()
        if selection == "":
            return None
        try:
            index = int(selection) - 1
            if 0 <= index < len(tasks):
                return tasks[index]
        except ValueError:
            pass
        console.print("[red]Please enter a valid task number.[/red]")


def get_all_projects(users):
    """Return all projects belonging to all users."""
    return [project for user in users for project in user.projects]


def interactive_menu():
    """Run the user-friendly interactive Project Manager menu."""

    while True:
        console.print(
            "\n[bold]========== PROJECT MANAGER ==========[/bold]"
        )
        console.print("1. Add User")
        console.print("2. List Users")
        console.print("3. Add Project")
        console.print("4. List Projects")
        console.print("5. Add Task")
        console.print("6. List Tasks")
        console.print("7. Complete Task")
        console.print("8. Edit Task")
        console.print("9. Delete Task")
        console.print("10. Exit")

        choice = input("\nEnter your choice: ").strip()

        # 1. Add User
        if choice == "1":
            console.print("\n[bold]Add a New User[/bold]")

            args = argparse.Namespace(
                username=prompt_required("Username: "),
                name=prompt_required("Full name: "),
                email=prompt_required("Email: "),
            )

            cmd_add_user(args)

        # 2. List Users
        elif choice == "2":
            cmd_list_users(argparse.Namespace())

        # 3. Add Project
        elif choice == "3":
            users = load_users()
            user = select_user(users)

            if user is None:
                continue

            console.print(
                f"\n[bold]Add Project for {user.name}[/bold]"
            )

            args = argparse.Namespace(
                username=user.username,
                title=prompt_required("Project title: "),
                description=input(
                    "Description (optional): "
                ).strip(),
                due_date=(
                    input(
                        "Due date "
                        "(optional, for example August 30 2026): "
                    ).strip()
                    or None
                ),
            )

            cmd_add_project(args)

        # 4. List Projects
        elif choice == "4":
            users = load_users()

            if not users:
                console.print("[yellow]No users found.[/yellow]")
                continue

            console.print("\n1. View all projects")
            console.print("2. View projects for one user")

            view_choice = input("Enter your choice: ").strip()

            if view_choice == "1":
                cmd_list_projects(
                    argparse.Namespace(username=None)
                )

            elif view_choice == "2":
                user = select_user(users)

                if user is not None:
                    cmd_list_projects(
                        argparse.Namespace(
                            username=user.username
                        )
                    )

            else:
                console.print("[red]Invalid option.[/red]")

        # 5. Add Task
        elif choice == "5":
            users = load_users()
            user = select_user(users)

            if user is None:
                continue

            project = select_project(user.projects)

            if project is None:
                continue

            console.print(
                f"\n[bold]Add Task to {project.title}[/bold]"
            )

            args = argparse.Namespace(
                username=user.username,
                project_id=project.project_id,
                title=prompt_required("Task title: "),
                description=input(
                    "Description (optional): "
                ).strip(),
                contributors=input(
                    "Contributors "
                    "(comma-separated, optional): "
                ).strip(),
            )

            cmd_add_task(args)

        # 6. List Tasks
        elif choice == "6":
            users = load_users()
            projects = get_all_projects(users)
            project = select_project(projects)

            if project is None:
                continue

            cmd_list_tasks(
                argparse.Namespace(
                    project_id=project.project_id
                )
            )

        # 7. Complete Task
        elif choice == "7":
            users = load_users()
            projects = get_all_projects(users)
            project = select_project(projects)

            if project is None:
                continue

            incomplete_tasks = [
                task
                for task in project.tasks
                if task.status.lower() != "completed"
            ]

            if not incomplete_tasks:
                console.print(
                    "[yellow]This project has no incomplete tasks.[/yellow]"
                )
                continue

            task = select_task(incomplete_tasks)

            if task is None:
                continue

            confirmation = input(
                f"Mark '{task.title}' as complete? (y/n): "
            ).strip().lower()

            if confirmation not in ("y", "yes"):
                console.print(
                    "[yellow]Task completion cancelled.[/yellow]"
                )
                continue

            cmd_complete_task(
                argparse.Namespace(
                    project_id=project.project_id,
                    task_id=task.task_id,
                )
            )

        # 8. Edit Task
        elif choice == "8":
            users = load_users()
            projects = get_all_projects(users)
            project = select_project(projects)

            if project is None:
                continue

            task = select_task(project.tasks)

            if task is None:
                continue

            console.print(
                f"\n[bold]Edit Task: {task.title}[/bold]"
            )
            console.print(
                "[dim]Press Enter to keep the current value.[/dim]"
            )

            new_title = input(
                f"New title [{task.title}]: "
            ).strip()

            current_description = (
                task.description
                if task.description
                else "No description"
            )

            new_description = input(
                f"New description [{current_description}]: "
            )

            args = argparse.Namespace(
                project_id=project.project_id,
                task_id=task.task_id,
                title=new_title or None,
                description=(
                    new_description.strip()
                    if new_description != ""
                    else None
                ),
            )

            cmd_edit_task(args)

        # 9. Delete Task
        elif choice == "9":
            users = load_users()
            projects = get_all_projects(users)
            project = select_project(projects)

            if project is None:
                continue

            task = select_task(project.tasks)

            if task is None:
                continue

            confirmation = input(
                f"Delete task '{task.title}' permanently? (y/n): "
            ).strip().lower()

            if confirmation not in ("y", "yes"):
                console.print(
                    "[yellow]Task deletion cancelled.[/yellow]"
                )
                continue

            cmd_delete_task(
                argparse.Namespace(
                    project_id=project.project_id,
                    task_id=task.task_id,
                )
            )

        # 10. Exit
        elif choice == "10":
            console.print(
                "\n[green]Thank you for using "
                "Project Manager. Goodbye![/green]"
            )
            break

        else:
            console.print(
                "[red]Invalid option. "
                "Please enter a number from 1 to 10.[/red]"
            )

if __name__ == "__main__":
    if len(sys.argv) == 1:
        interactive_menu()
    else:
        main()