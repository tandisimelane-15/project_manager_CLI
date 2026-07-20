from models.task import Task


class Project:
    """
    Represents a project that belongs to one user (one-to-many: User -> Projects)
    and contains many tasks (one-to-many: Project -> Tasks).
    """

    def __init__(self, project_id, title, description="", due_date=None, owner=None, tasks=None):
        self.project_id = project_id
        self.title = title
        self.description = description
        self.due_date = due_date  # store as string, e.g. "2026-08-01"
        self.owner = owner        # username of the user who owns this project
        self.tasks = tasks if tasks is not None else []  # list of Task objects

    def add_task(self, task: Task):
        self.tasks.append(task)

    def get_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def complete_task(self, task_id):
        task = self.get_task(task_id)
        if task:
            task.mark_complete()
            return True
        return False

    def to_dict(self):
        return {
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "owner": self.owner,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data):
        tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        return cls(
            project_id=data["project_id"],
            title=data["title"],
            description=data.get("description", ""),
            due_date=data.get("due_date"),
            owner=data.get("owner"),
            tasks=tasks,
        )

    def __repr__(self):
        return f"Project({self.project_id}, '{self.title}', owner={self.owner}, tasks={len(self.tasks)})"