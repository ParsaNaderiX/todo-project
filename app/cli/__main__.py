"""CLI entry point for the todo application using repository-backed services."""
from typing import List
import sys

from app.cli.utils import handle_application_error, display_error, confirm_action
from app.cli import (
    display_main_menu,
    display_add_project_menu,
    display_add_task_menu,
    display_edit_project_menu,
    display_edit_task_menu,
    display_edit_task_status_menu,
    display_welcome,
)

from app.db.session import get_db
from app.repositories import ProjectRepository, TaskRepository
from app.services import ProjectService, TaskService


def _read_int(prompt: str) -> int:
    while True:
        raw = input(prompt)
        try:
            return int(raw)
        except ValueError:
            print("Invalid input! Please enter a number.")


def _choose_id(prompt: str, valid_ids: List[int]) -> int:
    """Prompt the user to choose a numeric ID present in `valid_ids`.

    Args:
        prompt: Input prompt to show the user.
        valid_ids: List of allowed integer IDs.

    Returns:
        The chosen integer ID.

    Raises:
        ValueError: If `valid_ids` is empty.
    """
    if not valid_ids:
        raise ValueError("No items to choose from")
    while True:
        choice = _read_int(prompt)
        if choice in valid_ids:
            return choice
        print(f"Please enter one of the following IDs: {', '.join(map(str, valid_ids))}.")


def main():
    # Deprecation notice (visible but non-blocking)
    print("\nWARNING: The CLI is deprecated and will be removed in the next version.", file=sys.stderr)
    print("Please use the new REST API instead: http://localhost:8000", file=sys.stderr)
    print("API documentation: http://localhost:8000/docs\n", file=sys.stderr)

    # Obtain a DB session from the generator
    db = next(get_db())

    try:
        # Initialize repositories and services (dependency injection)
        project_repo = ProjectRepository(db)
        task_repo = TaskRepository(db)

        project_service = ProjectService(project_repo)
        task_service = TaskService(task_repo)

        display_welcome()

        while True:
            main_menu_option = display_main_menu()

            if main_menu_option == 1:
                name, description = display_add_project_menu()
                project = handle_application_error(project_service.create_project, name, description)
                if project is not None:
                    print(f"Project {project.name} created successfully (ID: {project.id})")
                continue

            elif main_menu_option == 2:
                projects = project_service.list_projects()
                if not projects:
                    print("No projects exist yet. Please create a project first.")
                    continue

                print("Select a project (enter the project ID):")
                ids = []
                for p in projects:
                    ids.append(p.id)
                    print(f"{p.id}. {p.name}")
                project_id = _choose_id("Enter project ID: ", ids)

                name, description, status, deadline = display_add_task_menu()
                task = handle_application_error(
                    task_service.create_task,
                    project_id,
                    name,
                    description,
                    status,
                    deadline,
                )
                if task is not None:
                    proj = handle_application_error(project_service.get_project, project_id)
                    proj_name = proj.name if proj is not None else str(project_id)
                    print(f"Task {task.name} added successfully to project {proj_name} (Task ID: {task.id})")
                continue

            elif main_menu_option == 3:
                projects = project_service.list_projects()
                if not projects:
                    print("No projects exist yet. Please create a project first.")
                    continue

                print("Select a project to edit (enter the project ID):")
                ids = []
                for p in projects:
                    ids.append(p.id)
                    print(f"{p.id}. {p.name}")
                project_id = _choose_id("Enter project ID: ", ids)

                new_name, new_description = display_edit_project_menu()
                project = handle_application_error(
                    project_service.edit_project,
                    project_id,
                    new_name,
                    new_description,
                )
                if project is not None:
                    print(f"Project {project.name} edited successfully")
                continue

            elif main_menu_option == 4:
                projects = project_service.list_projects()
                if not projects:
                    print("No projects exist yet. Please create a project first.")
                    continue

                print("Select a project (enter the project ID):")
                ids = []
                for p in projects:
                    ids.append(p.id)
                    print(f"{p.id}. {p.name}")
                project_id = _choose_id("Enter project ID: ", ids)

                tasks = task_service.list_tasks(project_id)
                if not tasks:
                    print("No tasks exist in this project yet. Please add a task first.")
                    continue

                print("Select a task to edit (enter the task ID):")
                task_ids = []
                for t in tasks:
                    task_ids.append(t.id)
                    print(f"{t.id}. {t.name}")
                task_id = _choose_id("Enter task ID: ", task_ids)

                new_name, new_description, new_status, new_deadline = display_edit_task_menu()
                task = handle_application_error(
                    task_service.edit_task,
                    project_id,
                    task_id,
                    new_name,
                    new_description,
                    new_status,
                    new_deadline,
                )
                if task is not None:
                    proj = handle_application_error(project_service.get_project, project_id)
                    proj_name = proj.name if proj is not None else str(project_id)
                    print(f"Task {task.name} edited successfully in project {proj_name}")
                continue

            elif main_menu_option == 5:
                projects = project_service.list_projects()
                if not projects:
                    print("No projects exist yet. Please create a project first.")
                    continue

                print("Select a project (enter the project ID):")
                ids = []
                for p in projects:
                    ids.append(p.id)
                    print(f"{p.id}. {p.name}")
                project_id = _choose_id("Enter project ID: ", ids)

                tasks = task_service.list_tasks(project_id)
                if not tasks:
                    print("No tasks exist in this project yet. Please add a task first.")
                    continue

                print("Select a task to update status (enter the task ID):")
                task_ids = []
                for t in tasks:
                    task_ids.append(t.id)
                    print(f"{t.id}. {t.name} (current status: {t.status})")
                task_id = _choose_id("Enter task ID: ", task_ids)

                new_status = display_edit_task_status_menu()
                task = handle_application_error(task_service.edit_task_status, project_id, task_id, new_status)
                if task is not None:
                    proj = handle_application_error(project_service.get_project, project_id)
                    proj_name = proj.name if proj is not None else str(project_id)
                    print(f"Task {task.name} status edited successfully in project {proj_name}")
                continue

            elif main_menu_option == 6:
                projects = project_service.list_projects()
                if not projects:
                    print("No projects exist yet. Please create a project first.")
                    continue

                print("Select a project to delete (enter the project ID):")
                ids = []
                for p in projects:
                    ids.append(p.id)
                    print(f"{p.id}. {p.name}")
                project_id = _choose_id("Enter project ID: ", ids)
                project = handle_application_error(project_service.get_project, project_id)

                if project is None:
                    continue

                if confirm_action(f"Are you sure you want to delete project '{project.name}'? This will delete all its tasks"):
                    if handle_application_error(project_service.delete_project, project_id) is not None:
                        print(f"Project {project.name} deleted successfully")
                continue

            elif main_menu_option == 7:
                projects = project_service.list_projects()
                if not projects:
                    print("No projects exist yet. Please create a project first.")
                    continue

                print("Select a project (enter the project ID):")
                ids = []
                for p in projects:
                    ids.append(p.id)
                    print(f"{p.id}. {p.name}")
                project_id = _choose_id("Enter project ID: ", ids)

                tasks = task_service.list_tasks(project_id)
                if not tasks:
                    print("No tasks exist in this project yet. Please add a task first.")
                    continue

                print("Select a task to delete (enter the task ID):")
                task_ids = []
                for t in tasks:
                    task_ids.append(t.id)
                    print(f"{t.id}. {t.name}")
                task_id = _choose_id("Enter task ID: ", task_ids)

                task = None
                for t in tasks:
                    if t.id == task_id:
                        task = t
                        break
                project = handle_application_error(project_service.get_project, project_id)

                if task is None or project is None:
                    continue

                if confirm_action(f"Are you sure you want to delete task '{task.name}' from project '{project.name}'?"):
                    if handle_application_error(task_service.delete_task, project_id, task_id) is not None:
                        print(f"Task {task.name} deleted successfully from project {project.name}")
                continue

            elif main_menu_option == 8:
                projects = project_service.list_projects()
                if not projects:
                    print("No projects to display.")
                    continue

                print("All projects:")
                for p in projects:
                    print(f"{p.id}. {p.name} - {p.description} | Tasks: {len(p.tasks)}")

            elif main_menu_option == 9:
                tasks = task_service.list_all_tasks()
                if not tasks:
                    print("No tasks to display.")
                    continue

                print("All tasks:")
                current_project = None
                for t in tasks:
                    proj_name = t.project.name if getattr(t, "project", None) else "<unknown>"
                    print(f"Project: {proj_name} (Project ID: {t.project_id})")
                    break
                # Group by project for display
                grouped = {}
                for t in tasks:
                    grouped.setdefault(t.project_id, []).append(t)

                for pid, tlist in grouped.items():
                    proj_name = tlist[0].project.name if getattr(tlist[0], "project", None) else str(pid)
                    print(f"Project: {proj_name} (ID: {pid})")
                    for t in tlist:
                        print(f"  {t.id}. {t.name} - {t.description} | Status: {t.status} | Deadline: {t.deadline}")

            elif main_menu_option == 10:
                print("Exiting... See you!")
                break

    except KeyboardInterrupt:
        # Ensure any open transaction is rolled back on user interrupt
        try:
            db.rollback()
        except Exception:
            pass
        print("\nProgram interrupted by user. Exiting...")
    except Exception as e:
        try:
            db.rollback()
        except Exception:
            pass
        display_error(f"Unexpected error occurred: {str(e)}")
    finally:
        try:
            db.close()
        except Exception:
            pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
    except Exception as e:
        display_error(f"Unexpected error occurred: {str(e)}")
        print("The application will now exit.")