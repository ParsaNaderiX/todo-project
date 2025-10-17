class Project:
    def __init__(self, name, description, tasks):
        self.name = name
        self.description = description
        self.tasks = tasks

    def edit_project(self, new_name, new_description):
        self.name = new_name
        self.description = new_description

    def delete_project(self):
        # Deletion is managed by storage
        return
    
    def add_task(self, name, description, status, deadline):
        task = Task(name, description, status, deadline, project=self)
        self.tasks.append(task)
    
    def delete_task(self, task):
        self.tasks.remove(task)
    

class Task:
    def __init__(self, name, description, status, deadline, project):
        self.name = name
        self.description = description
        self.status = status
        self.deadline = deadline
        self.project = project

    def edit_task(self, new_name, new_description, new_status, new_deadline):
        self.name = new_name
        self.description = new_description
        self.status = new_status
        self.deadline = new_deadline
    
    def edit_task_status(self, new_status):
        self.status = new_status