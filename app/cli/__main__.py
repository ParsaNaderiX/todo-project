"""CLI entry point for the todo application."""
from app.storage import InMemoryStorage
from app.services import TodoService
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

def _read_int(prompt: str) -> int:
    while True:
        raw = input(prompt)
        try:
            return int(raw)
        except ValueError:
            print("Invalid input! Please enter a number.")

def _choose_index(prompt: str, total_count: int) -> int:
    if total_count <= 0:
        raise ValueError("No items to choose from")
    while True:
        choice = _read_int(prompt)
        idx = choice - 1
        if 0 <= idx < total_count:
            return idx
        print(f"Please enter a number between 1 and {total_count}.")

def main():
    storage = InMemoryStorage()
    service = TodoService(storage)
    display_welcome()
    
    while True:
        main_menu_option = display_main_menu()

        if main_menu_option == 1:
            name, description = display_add_project_menu()
            project = handle_application_error(service.create_project, name, description)
            if project is not None:
                print(f"Project {project.name} created successfully")
            continue

        elif main_menu_option == 2:
            projects = service.list_projects()
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue
            
            print("Select a project:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name}")
            project_index = _choose_index("Enter project number: ", len(projects))

            name, description, status, deadline = display_add_task_menu()
            task = handle_application_error(
                service.create_task,
                project_index,
                name,
                description,
                status,
                deadline
            )
            if task is not None:
                print(f"Task {task.name} added successfully to project {projects[project_index].name}")
            continue

        elif main_menu_option == 3:
            projects = service.list_projects()
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue

            print("Select a project to edit:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name}")
            project_index = _choose_index("Enter project number: ", len(projects))

            new_name, new_description = display_edit_project_menu()
            # Validate non-empty and unique project name (excluding current project)
            project = handle_application_error(
                service.edit_project,
                project_index,
                new_name,
                new_description
            )
            if project is not None:
                print(f"Project {project.name} edited successfully")
            continue

        elif main_menu_option == 4:
            projects = service.list_projects()
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue

            print("Select a project:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name}")
            project_index = _choose_index("Enter project number: ", len(projects))

            tasks = service.list_tasks(project_index)
            if not tasks:
                print("No tasks exist in this project yet. Please add a task first.")
                continue

            print("Select a task to edit:")
            for idx, t in enumerate(tasks, 1):
                print(f"{idx}. {t.name}")
            task_index = _choose_index("Enter task number: ", len(tasks))

            new_name, new_description, new_status, new_deadline = display_edit_task_menu()
            task = handle_application_error(
                service.edit_task,
                project_index,
                task_index,
                new_name,
                new_description,
                new_status,
                new_deadline
            )
            if task is not None:
                print(f"Task {task.name} edited successfully in project {projects[project_index].name}")
            continue

        elif main_menu_option == 5:
            projects = service.list_projects()
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue

            print("Select a project:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name}")
            project_index = _choose_index("Enter project number: ", len(projects))

            tasks = service.list_tasks(project_index)
            if not tasks:
                print("No tasks exist in this project yet. Please add a task first.")
                continue

            print("Select a task to update status:")
            for idx, t in enumerate(tasks, 1):
                print(f"{idx}. {t.name} (current status: {t.status})")
            task_index = _choose_index("Enter task number: ", len(tasks))

            new_status = display_edit_task_status_menu()
            task = handle_application_error(service.edit_task_status, project_index, task_index, new_status)
            if task is not None:
                print(f"Task {task.name} status edited successfully in project {projects[project_index].name}")
            continue

        elif main_menu_option == 6:
            projects = service.list_projects()
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue

            print("Select a project to delete:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name}")
            project_index = _choose_index("Enter project number: ", len(projects))
            project = projects[project_index]
            
            if confirm_action(f"Are you sure you want to delete project '{project.name}'? This will delete all its tasks"):
                if handle_application_error(service.delete_project, project_index) is not None:
                    print(f"Project {project.name} deleted successfully")
            continue

        elif main_menu_option == 7:
            projects = service.list_projects()
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue

            print("Select a project:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name}")
            project_index = _choose_index("Enter project number: ", len(projects))

            tasks = service.list_tasks(project_index)
            if not tasks:
                print("No tasks exist in this project yet. Please add a task first.")
                continue

            print("Select a task to delete:")
            for idx, t in enumerate(tasks, 1):
                print(f"{idx}. {t.name}")
            task_index = _choose_index("Enter task number: ", len(tasks))
            task = tasks[task_index]
            project = projects[project_index]
            
            if confirm_action(f"Are you sure you want to delete task '{task.name}' from project '{project.name}'?"):
                if handle_application_error(service.delete_task, project_index, task_index) is not None:
                    print(f"Task {task.name} deleted successfully from project {project.name}")
            continue

        elif main_menu_option == 8:
            projects = service.list_projects()
            if not projects:
                print("No projects to display.")
                continue

            print("All projects:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name} - {p.description} | Tasks: {len(p.tasks)}")

        elif main_menu_option == 9:
            projects = storage.list_projects()
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue

            print("All tasks:")
            has_any_task = False
            for p in projects:
                if not p.tasks:
                    continue
                print(f"Project: {p.name}")
                for idx, t in enumerate(p.tasks, 1):
                    has_any_task = True
                    print(f"  {idx}. {t.name} - {t.description} | Status: {t.status} | Deadline: {t.deadline}")
            if not has_any_task:
                print("No tasks to display.")

        elif main_menu_option == 10:
            print("Exiting... See you!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
    except Exception as e:
        display_error(f"Unexpected error occurred: {str(e)}")
        print("The application will now exit.")