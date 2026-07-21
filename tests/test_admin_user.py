import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User
from models.project import Project
from models.admin_user import AdminUser


def test_admin_user_is_a_user():
    admin = AdminUser(username="root", name="Admin", email="admin@example.com")
    assert isinstance(admin, User)
    assert admin.is_admin is True


def test_admin_can_remove_others_project():
    admin = AdminUser(username="root", name="Admin", email="admin@example.com")
    alice = User(username="alice", name="Alice Smith", email="alice@example.com")
    project = Project(project_id="p1", title="Site Redesign", owner="alice")
    alice.add_project(project)

    result = admin.remove_project_from(alice, "p1")
    assert result is True
    assert alice.get_project("p1") is None