"""Domain models for the todo application."""
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
    project: Project

    def edit_task(self, new_name: str, new_description: str, new_status: str, new_deadline: str) -> None:
        """Update task details.
        
        Args:
            new_name: The new name for the task
            new_description: The new description
            new_status: New status (must be 'todo', 'doing', or 'done')
            new_deadline: New deadline in YYYY-MM-DD format
        """
        self.name = new_name
        self.description = new_description
        self.status = new_status
        self.deadline = new_deadline
    
    def edit_task_status(self, new_status: str) -> None:
        """Update just the task status.
        
        Args:
            new_status: New status (must be 'todo', 'doing', or 'done')
        """
        self.status = new_status


@dataclass
class Project:
    """Represents a project containing tasks."""
    name: str
    description: str
    tasks: List[Task] = field(default_factory=list)

    def edit_project(self, new_name: str, new_description: str) -> None:
        """Update project details.
        
        Args:
            new_name: The new name for the project
            new_description: The new description
        """
        self.name = new_name
        self.description = new_description
    
    def add_task(self, name: str, description: str, status: str, deadline: str) -> Task:
        """Add a new task to the project.
        
        Args:
            name: Task name
            description: Task description
            status: Initial status ('todo', 'doing', 'done')
            deadline: Due date in YYYY-MM-DD format
            
        Returns:
            The newly created task
        """
        task = Task(name, description, status, deadline, project=self)
        self.tasks.append(task)
        return task
    
    def delete_task(self, task: Task) -> None:
        """Remove a task from the project.
        
        Args:
            task: The task to remove
        """
        self.tasks.remove(task)


