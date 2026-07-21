from models.user import User


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

    def to_dict(self):
        data = super().to_dict()
        data["is_admin"] = True
        return data

    def __repr__(self):
        return f"AdminUser({self.username}, '{self.name}', projects={len(self.projects)})"