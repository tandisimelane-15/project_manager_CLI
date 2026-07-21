import argparse

import main
from models.project import Project
from models.task import Task
from models.user import User


def create_sample_data():
    user = User(
        username="alice",
        name="Alice Smith",
        email="alice@example.com",
    )

    project = Project(
        project_id="project-1",
        title="Website Redesign",
        description="Redesign the website",
        due_date=None,
        owner="alice",
    )

    task = Task(
        task_id="task-1",
        title="Design Homepage",
        description="Create the homepage design",
        contributors=["Alice"],
    )

    project.add_task(task)
    user.add_project(project)

    return [user], project, task


def mock_storage(monkeypatch, users):
    saved_data = []

    monkeypatch.setattr(main, "load_users", lambda: users)

    monkeypatch.setattr(
        main,
        "save_users",
        lambda updated_users: saved_data.append(updated_users),
    )

    return saved_data


def test_edit_task(monkeypatch):
    users, project, task = create_sample_data()
    saved_data = mock_storage(monkeypatch, users)

    args = argparse.Namespace(
        project_id="project-1",
        task_id="task-1",
        title="Develop Homepage",
        description="Build the homepage",
    )

    main.cmd_edit_task(args)

    assert task.title == "Develop Homepage"
    assert task.description == "Build the homepage"
    assert len(saved_data) == 1


def test_delete_task(monkeypatch):
    users, project, task = create_sample_data()
    saved_data = mock_storage(monkeypatch, users)

    args = argparse.Namespace(
        project_id="project-1",
        task_id="task-1",
    )

    main.cmd_delete_task(args)

    assert task not in project.tasks
    assert len(saved_data) == 1