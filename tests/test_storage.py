import sys
import os


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import storage
from models.user import User
from models.project import Project
from models.admin_user import AdminUser

def test_save_and_load_roundtrip(tmp_path, monkeypatch):
    test_file = tmp_path / "test_data.json"
    monkeypatch.setattr(storage, "DATA_FILE", str(test_file))

    user = User(username="alice", name="Alice Wacera", email="alice@example.com")
    project = Project(project_id="p1", title="Site Redesign", owner="alice")
    user.add_project(project)

    storage.save_users([user])
    loaded = storage.load_users()

    assert len(loaded) == 1
    assert loaded[0].username == "alice"
    assert loaded[0].projects[0].project_id == "p1"


def test_load_users_returns_empty_list_when_no_file(tmp_path, monkeypatch):
    missing_file = tmp_path / "does_not_exist.json"
    monkeypatch.setattr(storage, "DATA_FILE", str(missing_file))
    assert storage.load_users() == []

def test_admin_user_remains_admin_after_loading(tmp_path):
    """
    An AdminUser should remain an AdminUser after saving and loading.
    """
    file_path = tmp_path / "users.json"

    admin = AdminUser(
        username="admin1",
        name="System Admin",
        email="admin@example.com",
    )

    storage.DATA_FILE = str(file_path)

    storage.save_users([admin])
    loaded_users = storage.load_users()

    assert len(loaded_users) == 1
    assert isinstance(loaded_users[0], AdminUser)
    assert loaded_users[0].is_admin is True