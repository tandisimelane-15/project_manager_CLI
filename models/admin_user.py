from models.user import User
from models.project import Project


class AdminUser(User):
    """
    An AdminUser is a User with elevated permissions — they can remove
    any project system-wide, not just its own.
    """

    def __init__(self, username, name, email, projects=None):
        super().__init__(username, name, email, projects)
        self.is_admin = True

    def remove_project_from(self, target_user, project_id):
        """Admins can remove a project from any user's account."""
        project = target_user.get_project(project_id)
        if project:
            target_user.projects.remove(project)
            return True
        return False
    @classmethod
    def from_dict(cls, data):
        """
        Rebuild an AdminUser object from dictionary data.
        """
        projects = [
        Project.from_dict(project_data)
        for project_data in data.get("projects", [])
        ]

        return cls(
            username=data["username"],
            name=data["name"],
            email=data["email"],
            projects=projects,
        )
    def to_dict(self):
        data = super().to_dict()
        data["is_admin"] = True
        return data

    def __repr__(self):
        return f"AdminUser({self.username}, '{self.name}', projects={len(self.projects)})"