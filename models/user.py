from models.project import Project


class User:
    """
    Represents a user who owns many projects (one-to-many: User -> Projects).
    """

    def __init__(self, username, name, email, projects=None):
        self.username = username  # used as a unique id for this user
        self.name = name
        self.email = email
        self.projects = projects if projects is not None else []  # list of Project objects

    def add_project(self, project: Project):
        self.projects.append(project)

    def get_project(self, project_id):
        for project in self.projects:
            if project.project_id == project_id:
                return project
        return None

    def to_dict(self):
        return {
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "projects": [project.to_dict() for project in self.projects],
        }

    @classmethod
    def from_dict(cls, data):
        projects = [Project.from_dict(p) for p in data.get("projects", [])]
        return cls(
            username=data["username"],
            name=data["name"],
            email=data["email"],
            projects=projects,
        )

    def __repr__(self):
        return f"User({self.username}, '{self.name}', projects={len(self.projects)})"