from typing import List, Optional, Any
from datetime import datetime, date
from app.config import MAX_NUMBER_OF_PROJECT, MAX_NUMBER_OF_TASK


class InMemoryStorage:
    def __init__(self):
        self.projects: List[Any] = []

    def add_project(self, project: Any) -> None:
        if not getattr(project, "name", None) or str(project.name).strip() == "":
            raise ValueError("Project name is required.")
        name_word_count = len(str(project.name).strip().split())
        desc_word_count = len(str(getattr(project, "description", "")).strip().split())
        if name_word_count > 30:
            raise ValueError("Project name must be <= 30 words.")
        if desc_word_count > 150:
            raise ValueError("Project description must be <= 150 words.")
        if any(existing.name == project.name for existing in self.projects):
            raise ValueError("Project name must be unique.")
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
        if hasattr(project, "tasks") and isinstance(project.tasks, list):
            project.tasks.clear()
        del self.projects[index]

    def add_task(self, project_index: int, task: Any) -> None:
        project = self.get_project(project_index)
        if project is None:
            raise IndexError("Project index out of range")
        if not getattr(task, "name", None) or str(task.name).strip() == "":
            raise ValueError("Task name is required.")
        allowed_status = {"todo", "doing", "done"}
        status_value = getattr(task, "status", None)
        if status_value is None or str(status_value).strip() == "":
            task.status = "todo"
        else:
            normalized = str(status_value).strip().lower()
            if normalized not in allowed_status:
                raise ValueError("Task status must be one of: todo, doing, done.")
            task.status = normalized
        deadline_value = getattr(task, "deadline", None)
        if deadline_value is not None and str(deadline_value).strip() != "":
            try:
                parsed = datetime.strptime(str(deadline_value).strip(), "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Task deadline must be in YYYY-MM-DD format.")
            if parsed < date.today():
                raise ValueError("Task deadline cannot be in the past.")
        name_word_count = len(str(task.name).strip().split())
        desc_word_count = len(str(getattr(task, "description", "")).strip().split())
        if name_word_count > 30:
            raise ValueError("Task name must be <= 30 words.")
        if desc_word_count > 150:
            raise ValueError("Task description must be <= 150 words.")
        if any(existing.name == task.name for existing in project.tasks):
            raise ValueError("Task name must be unique within its project.")
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


