from typing import List
from app.ports import StoragePort
from app.core import Project, Task


class TodoService:
    def __init__(self, storage: StoragePort):
        self.storage = storage

    def create_project(self, name: str, description: str) -> Project:
        project = Project(name, description, [])
        self.storage.add_project(project)
        return project

    def list_projects(self) -> List[Project]:
        return self.storage.list_projects()  # type: ignore[return-value]

    def edit_project(self, index: int, new_name: str, new_description: str) -> Project:
        project = self._get_project_or_raise(index)
        project.edit_project(new_name, new_description)
        return project

    def delete_project(self, index: int) -> None:
        self.storage.delete_project(index)

    def create_task(self, project_index: int, name: str, description: str, status: str, deadline: str) -> Task:
        project = self._get_project_or_raise(project_index)
        task = Task(name, description, status, deadline, project=project)
        self.storage.add_task(project_index, task)
        return task

    def list_tasks(self, project_index: int) -> List[Task]:
        return self.storage.list_tasks(project_index)  # type: ignore[return-value]

    def edit_task(self, project_index: int, task_index: int, new_name: str, new_description: str, new_status: str, new_deadline: str) -> Task:
        task = self._get_task_or_raise(project_index, task_index)
        task.edit_task(new_name, new_description, new_status, new_deadline)
        return task

    def edit_task_status(self, project_index: int, task_index: int, new_status: str) -> Task:
        task = self._get_task_or_raise(project_index, task_index)
        task.edit_task_status(new_status)
        return task

    def delete_task(self, project_index: int, task_index: int) -> None:
        self.storage.delete_task(project_index, task_index)

    def _get_project_or_raise(self, index: int) -> Project:
        project = self.storage.get_project(index)
        if project is None:
            raise IndexError("Project index out of range")
        return project  # type: ignore[return-value]

    def _get_task_or_raise(self, project_index: int, task_index: int) -> Task:
        task = self.storage.get_task(project_index, task_index)
        if task is None:
            raise IndexError("Task or project index out of range")
        return task  # type: ignore[return-value]


