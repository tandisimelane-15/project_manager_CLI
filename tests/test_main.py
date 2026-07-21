import os
import sys
from types import SimpleNamespace

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)

import main
from models.user import User


def test_parser_contains_all_commands():
    parser = main.build_parser()

    command_arguments = {
        "add-user": [
            "--username", "alice",
            "--name", "Alice Smith",
            "--email", "alice@example.com",
        ],
        "list-users": [],
        "add-project": [
            "--username", "alice",
            "--title", "Website Redesign",
        ],
        "list-projects": [
            "--username", "alice",
        ],
        "add-task": [
            "--username", "alice",
            "--project-id", "project-1",
            "--title", "Design homepage",
        ],
        "list-tasks": [
            "--project-id", "project-1",
        ],
        "complete-task": [
            "--project-id", "project-1",
            "--task-id", "task-1",
        ],
    }

    for command, arguments in command_arguments.items():
        args = parser.parse_args([command, *arguments])

        assert args.command == command
        assert callable(args.func)

def test_find_user_is_case_insensitive():
    users = [
        User(
            username="alice",
            name="Alice Smith",
            email="alice@example.com",
        )
    ]

    result = main.find_user(users, "ALICE")

    assert result is users[0]


def test_add_user_saves_new_user(monkeypatch):
    saved_users = []

    monkeypatch.setattr(main, "load_users", lambda: [])

    def fake_save_users(users):
        saved_users.extend(users)

    monkeypatch.setattr(main, "save_users", fake_save_users)

    args = SimpleNamespace(
        username="alice",
        name="Alice Smith",
        email="alice@example.com",
    )

    main.cmd_add_user(args)

    assert len(saved_users) == 1
    assert saved_users[0].username == "alice"
    assert saved_users[0].name == "Alice Smith"
    assert saved_users[0].email == "alice@example.com"


def test_duplicate_user_is_not_saved(monkeypatch):
    existing_user = User(
        username="alice",
        name="Alice Smith",
        email="alice@example.com",
    )

    save_was_called = False

    monkeypatch.setattr(main, "load_users", lambda: [existing_user])

    def fake_save_users(users):
        nonlocal save_was_called
        save_was_called = True

    monkeypatch.setattr(main, "save_users", fake_save_users)

    args = SimpleNamespace(
        username="ALICE",
        name="Another Alice",
        email="another@example.com",
    )

    main.cmd_add_user(args)

    assert save_was_called is False