from core import Project
from CLI import (
    display_main_menu,
    display_add_project_menu,
    display_add_task_menu,
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
        
        else:
            pass

if __name__ == "__main__":
    main()