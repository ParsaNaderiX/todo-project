class Project:
    def __init__(self, name, description, tasks):
        self.name = name
        self.description = description
        self.tasks = tasks
        print(f"Project {self.name} created successfully")

    def edit_project(self, new_name, new_description):
        self.name = new_name
        self.description = new_description
        print(f"Project {self.name} edited successfully")

    def delete_project(self):
        project_name = self.name
        self.name = None
        self.description = None
        self.tasks = None
        print(f"Project {project_name} deleted successfully")
    
    def add_task(self, name, description, status, deadline):
        task = Task(name, description, status, deadline, project=self)
        self.tasks.append(task)
        print(f"Task {task.name} added successfully to project {self.name}")
    
    def delete_task(self, task):
        self.tasks.remove(task)
        print(f"Task {task.name} deleted successfully from project {self.name}")
    

class Task:
    def __init__(self, name, description, status, deadline, project):
        self.name = name
        self.description = description
        self.status = status
        self.deadline = deadline
        self.project = project
        print(f"Task {self.name} created successfully in project {self.project.name}")

    def edit_task(self, new_name, new_description, new_status, new_deadline):
        self.name = new_name
        self.description = new_description
        self.status = new_status
        self.deadline = new_deadline
        print(f"Task {self.name} edited successfully in project {self.project.name}")
    
    def edit_task_status(self, new_status):
        self.status = new_status
        print(f"Task {self.name} status edited successfully in project {self.project.name}")