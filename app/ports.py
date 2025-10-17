from typing import Protocol, List, Optional, Any


class StoragePort(Protocol):
    def add_project(self, project: Any) -> None:
        ...

    def list_projects(self) -> List[Any]:
        ...

    def get_project(self, index: int) -> Optional[Any]:
        ...

    def delete_project(self, index: int) -> None:
        ...

    def add_task(self, project_index: int, task: Any) -> None:
        ...

    def list_tasks(self, project_index: int) -> List[Any]:
        ...

    def get_task(self, project_index: int, task_index: int) -> Optional[Any]:
        ...

    def delete_task(self, project_index: int, task_index: int) -> None:
        ...


