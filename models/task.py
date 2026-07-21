class Task:
    """
    Represents a single task inside a project.
    A task can have multiple contributors (many-to-many: Task <-> User).
    """

    def __init__(self, task_id, title, description="", contributors=None, status="pending"):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.contributors = contributors if contributors is not None else []
        self.status = status  # "pending" or "complete"

    def mark_complete(self):
        self.status = "complete"

    def edit(self, title=None, description=None):
        if title is not None and title.strip():
            self.title = title.strip()

        if description is not None:
            self.description = description.strip()

    def add_contributor(self, username):
        if username not in self.contributors:
            self.contributors.append(username)

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "contributors": self.contributors,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            task_id=data["task_id"],
            title=data["title"],
            description=data.get("description", ""),
            contributors=data.get("contributors", []),
            status=data.get("status", "pending"),
        )

    def __repr__(self):
        return f"Task({self.task_id}, '{self.title}', status={self.status}, contributors={self.contributors})"