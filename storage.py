from typing import List, Optional, Any
from config import MAX_NUMBER_OF_PROJECT, MAX_NUMBER_OF_TASK

class InMemoryStorage:
    def __init__(self):
        self.projects: List[Any] = []

    # Project operations
    def add_project(self, project: Any) -> None:
        if len(self.projects) >= MAX_NUMBER_OF_PROJECT:
            raise ValueError("Reached MAX_NUMBER_OF_PROJECT; cannot add more projects.")
        self.projects.append(project)

    def list_projects(self) -> List[Any]:
        return list(self.projects)

    def get_project(self, index: int) -> Optional[Any]:
        if 0 <= index < len(self.projects):
            return self.projects[index]
        return None

    def delete_project(self, index: int) -> None:
        project = self.get_project(index)
        if project is None:
            raise IndexError("Project index out of range")
        del self.projects[index]

    # Task operations
    def add_task(self, project_index: int, task: Any) -> None:
        project = self.get_project(project_index)
        if project is None:
            raise IndexError("Project index out of range")
        if len(project.tasks) >= MAX_NUMBER_OF_TASK:
            raise ValueError("Reached MAX_NUMBER_OF_TASK; cannot add more tasks to this project.")
        project.tasks.append(task)

    def list_tasks(self, project_index: int) -> List[Any]:
        project = self.get_project(project_index)
        if project is None:
            raise IndexError("Project index out of range")
        return list(project.tasks)

    def get_task(self, project_index: int, task_index: int) -> Optional[Any]:
        project = self.get_project(project_index)
        if project is None:
            return None
        if 0 <= task_index < len(project.tasks):
            return project.tasks[task_index]
        return None

    def delete_task(self, project_index: int, task_index: int) -> None:
        project = self.get_project(project_index)
        task = self.get_task(project_index, task_index)
        if project is None or task is None:
            raise IndexError("Task or project index out of range")
        del project.tasks[task_index]
