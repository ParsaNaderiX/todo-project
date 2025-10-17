from storage import InMemoryStorage
from core import Project, Task
from CLI import (
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
    display_welcome()
    
    while True:
        main_menu_option = display_main_menu()

        if main_menu_option == 1:
            name, description = display_add_project_menu()
            project = Project(name, description, [])
            storage.add_project(project)
            print(f"Project {project.name} created successfully")

        elif main_menu_option == 2:
            projects = storage.list_projects()
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue
            
            print("Select a project:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name}")
            project_index = _choose_index("Enter project number: ", len(projects))

            name, description, status, deadline = display_add_task_menu()
            task = Task(name, description, status, deadline, project=projects[project_index])
            storage.add_task(project_index, task)
            print(f"Task {task.name} added successfully to project {projects[project_index].name}")

        elif main_menu_option == 3:
            projects = storage.list_projects()
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue

            print("Select a project to edit:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name}")
            project_index = _choose_index("Enter project number: ", len(projects))

            new_name, new_description = display_edit_project_menu()
            project = projects[project_index]
            project.edit_project(new_name, new_description)
            print(f"Project {project.name} edited successfully")

        elif main_menu_option == 4:
            projects = storage.list_projects()
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue

            print("Select a project:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name}")
            project_index = _choose_index("Enter project number: ", len(projects))

            tasks = storage.list_tasks(project_index)
            if not tasks:
                print("No tasks exist in this project yet. Please add a task first.")
                continue

            print("Select a task to edit:")
            for idx, t in enumerate(tasks, 1):
                print(f"{idx}. {t.name}")
            task_index = _choose_index("Enter task number: ", len(tasks))

            new_name, new_description, new_status, new_deadline = display_edit_task_menu()
            task = tasks[task_index]
            task.edit_task(new_name, new_description, new_status, new_deadline)
            print(f"Task {task.name} edited successfully in project {projects[project_index].name}")

        elif main_menu_option == 5:
            projects = storage.list_projects()
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue

            print("Select a project:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name}")
            project_index = _choose_index("Enter project number: ", len(projects))

            tasks = storage.list_tasks(project_index)
            if not tasks:
                print("No tasks exist in this project yet. Please add a task first.")
                continue

            print("Select a task to update status:")
            for idx, t in enumerate(tasks, 1):
                print(f"{idx}. {t.name} (current status: {t.status})")
            task_index = _choose_index("Enter task number: ", len(tasks))

            new_status = display_edit_task_status_menu()
            task = tasks[task_index]
            task.edit_task_status(new_status)
            print(f"Task {task.name} status edited successfully in project {projects[project_index].name}")

        elif main_menu_option == 6:
            projects = storage.list_projects()
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue

            print("Select a project to delete:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name}")
            project_index = _choose_index("Enter project number: ", len(projects))
            project = projects[project_index]
            storage.delete_project(project_index)
            print(f"Project {project.name} deleted successfully")

        elif main_menu_option == 7:
            projects = storage.list_projects()
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue

            print("Select a project:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name}")
            project_index = _choose_index("Enter project number: ", len(projects))

            tasks = storage.list_tasks(project_index)
            if not tasks:
                print("No tasks exist in this project yet. Please add a task first.")
                continue

            print("Select a task to delete:")
            for idx, t in enumerate(tasks, 1):
                print(f"{idx}. {t.name}")
            task_index = _choose_index("Enter task number: ", len(tasks))
            task = tasks[task_index]
            project = projects[project_index]
            storage.delete_task(project_index, task_index)
            print(f"Task {task.name} deleted successfully from project {project.name}")

        elif main_menu_option == 8:
            projects = storage.list_projects()
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
    main()