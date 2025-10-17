def display_main_menu():
    print("Welcome to the To-Do List Application!")
    print("Please select an option:")
    print("1. Add a new project")
    print("2. Add a new task")
    print("3. Edit a project")
    print("4. Edit a task")
    print("5. Edit task status")
    print("6. Delete a project")
    print("7. Delete a task")
    print("8. View all projects")
    print("9. View all tasks")
    print("10. Exit")
    while True:
        option = input("Enter your choice: ")
        try:
            return int(option)
        except ValueError:
            print("Invalid input! Please enter a number from the options above.")

def display_add_project_menu():
    print("Please enter the project name:")
    name = input()
    print("Please enter the project description:")
    description = input()
    return name, description

def display_add_task_menu():
    print("Please enter the task name:")
    name = input()
    print("Please enter the task description:")
    description = input()
    print("Please enter the task status:")
    status = input()
    print("Please enter the task deadline:")
    deadline = input()
    return name, description, status, deadline


def display_edit_project_menu():
    print("Enter new project name:")
    new_name = input()
    print("Enter new project description:")
    new_description = input()
    return new_name, new_description


def display_edit_task_menu():
    print("Enter new task name:")
    new_name = input()
    print("Enter new task description:")
    new_description = input()
    print("Enter new task status:")
    new_status = input()
    print("Enter new task deadline:")
    new_deadline = input()
    return new_name, new_description, new_status, new_deadline


def display_edit_task_status_menu():
    print("Enter new task status:")
    new_status = input()
    return new_status