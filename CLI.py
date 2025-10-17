def display_main_menu():
    print("Welcome to the To-Do List Application!")
    print("Please select an option:")
    print("1. Add a new project")
    print("2. Add a new task")
    print("3. View all projects")
    print("4. View all tasks")
    print("5. Exit")
    while True:
        option = input("Enter your choice: ")
        try:
            return int(option)
        except ValueError:
            print("Invalid input! Please enter a number from the options above.")
