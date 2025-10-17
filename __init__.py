from core import Project
from CLI import (
    display_main_menu,
    display_add_project_menu,
    display_add_task_menu,
    display_edit_project_menu,
    display_edit_task_menu,
    display_edit_task_status_menu,
)

def main():
    projects = []
    
    while True:
        main_menu_option = display_main_menu()

        if main_menu_option == 1:
            name, description = display_add_project_menu()
            project = Project(name, description, [])
            projects.append(project)

        elif main_menu_option == 2:
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue
            
            print("Select a project:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name}")
            project_index = int(input("Enter project number: ")) - 1
            project = projects[project_index]

            name, description, status, deadline = display_add_task_menu()
            project.add_task(name, description, status, deadline)

        elif main_menu_option == 3:
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue

            print("Select a project to edit:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name}")
            project_index = int(input("Enter project number: ")) - 1
            project = projects[project_index]

            new_name, new_description = display_edit_project_menu()
            project.edit_project(new_name, new_description)

        elif main_menu_option == 4:
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue

            print("Select a project:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name}")
            project_index = int(input("Enter project number: ")) - 1
            project = projects[project_index]

            if not project.tasks:
                print("No tasks exist in this project yet. Please add a task first.")
                continue

            print("Select a task to edit:")
            for idx, t in enumerate(project.tasks, 1):
                print(f"{idx}. {t.name}")
            task_index = int(input("Enter task number: ")) - 1
            task = project.tasks[task_index]

            new_name, new_description, new_status, new_deadline = display_edit_task_menu()
            task.edit_task(new_name, new_description, new_status, new_deadline)

        elif main_menu_option == 5:
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue

            print("Select a project:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name}")
            project_index = int(input("Enter project number: ")) - 1
            project = projects[project_index]

            if not project.tasks:
                print("No tasks exist in this project yet. Please add a task first.")
                continue

            print("Select a task to update status:")
            for idx, t in enumerate(project.tasks, 1):
                print(f"{idx}. {t.name} (current status: {t.status})")
            task_index = int(input("Enter task number: ")) - 1
            task = project.tasks[task_index]

            new_status = display_edit_task_status_menu()
            task.edit_task_status(new_status)

        elif main_menu_option == 6:
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue

            print("Select a project to delete:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name}")
            project_index = int(input("Enter project number: ")) - 1
            project = projects[project_index]

            project.delete_project()
            del projects[project_index]

        elif main_menu_option == 7:
            if not projects:
                print("No projects exist yet. Please create a project first.")
                continue

            print("Select a project:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name}")
            project_index = int(input("Enter project number: ")) - 1
            project = projects[project_index]

            if not project.tasks:
                print("No tasks exist in this project yet. Please add a task first.")
                continue

            print("Select a task to delete:")
            for idx, t in enumerate(project.tasks, 1):
                print(f"{idx}. {t.name}")
            task_index = int(input("Enter task number: ")) - 1
            task = project.tasks[task_index]

            project.delete_task(task)

        elif main_menu_option == 8:
            if not projects:
                print("No projects to display.")
                continue

            print("All projects:")
            for idx, p in enumerate(projects, 1):
                print(f"{idx}. {p.name} - {p.description} | Tasks: {len(p.tasks)}")

        elif main_menu_option == 9:
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