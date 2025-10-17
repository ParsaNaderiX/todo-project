from typing import List, Optional, Any
from config import MAX_NUMBER_OF_PROJECT, MAX_NUMBER_OF_TASK

class InMemoryStorage:
    def __init__(self):
        self.projects: List[Any] = []

    # Project operations
    def add_project(self, project: Any) -> None:
        # Validate non-empty name
        if not getattr(project, "name", None) or str(project.name).strip() == "":
            raise ValueError("Project name is required.")
        # Word limits: name <= 30 words, description <= 150 words
        name_word_count = len(str(project.name).strip().split())
        desc_word_count = len(str(getattr(project, "description", "")).strip().split())
        if name_word_count > 30:
            raise ValueError("Project name must be <= 30 words.")
        if desc_word_count > 150:
            raise ValueError("Project description must be <= 150 words.")
        # Validate uniqueness across projects
        if any(existing.name == project.name for existing in self.projects):
            raise ValueError("Project name must be unique.")
        # Enforce cap
        if len(self.projects) >= MAX_NUMBER_OF_PROJECT:
            raise ValueError(f"Reached MAX_NUMBER_OF_PROJECT ({MAX_NUMBER_OF_PROJECT}); cannot add more projects.")
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
        # Validate non-empty name
        if not getattr(task, "name", None) or str(task.name).strip() == "":
            raise ValueError("Task name is required.")
        # Word limits: name <= 30 words, description <= 150 words
        name_word_count = len(str(task.name).strip().split())
        desc_word_count = len(str(getattr(task, "description", "")).strip().split())
        if name_word_count > 30:
            raise ValueError("Task name must be <= 30 words.")
        if desc_word_count > 150:
            raise ValueError("Task description must be <= 150 words.")
        # Validate uniqueness within the project
        if any(existing.name == task.name for existing in project.tasks):
            raise ValueError("Task name must be unique within its project.")
        # Enforce cap per project
        if len(project.tasks) >= MAX_NUMBER_OF_TASK:
            raise ValueError(f"Reached MAX_NUMBER_OF_TASK ({MAX_NUMBER_OF_TASK}); cannot add more tasks to this project.")
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
