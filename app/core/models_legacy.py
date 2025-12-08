"""Legacy domain dataclasses for the todo application.

This file is a backup of the previous `app.core.models` dataclasses and was
created automatically when the original file was removed. It is safe to delete
this backup once you are confident the codebase no longer needs the dataclasses.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


@dataclass
class Task:
    """Represents a task within a project."""
    name: str
    description: str
    status: str
    deadline: Optional[str]
    project: 'Project'

    def edit_task(self, new_name: str, new_description: str, new_status: str, new_deadline: str) -> None:
        self.name = new_name
        self.description = new_description
        self.status = new_status
        self.deadline = new_deadline

    def edit_task_status(self, new_status: str) -> None:
        self.status = new_status


@dataclass
class Project:
    """Represents a project containing tasks."""
    name: str
    description: str
    tasks: List[Task] = field(default_factory=list)

    def edit_project(self, new_name: str, new_description: str) -> None:
        self.name = new_name
        self.description = new_description

    def add_task(self, name: str, description: str, status: str, deadline: str) -> Task:
        task = Task(name, description, status, deadline, project=self)
        self.tasks.append(task)
        return task

    def delete_task(self, task: Task) -> None:
        self.tasks.remove(task)

