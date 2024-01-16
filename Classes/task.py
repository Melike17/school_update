from datetime import datetime
import json

class Task():
    FILE_PATH = "data/tasks.txt"

    def __init__(self,task_name,due_date,assigned_to_email,created_by,status="Open",created=None) -> None:
        self.task_name = task_name
        self.due_date = due_date
        self.assigned_to_email = assigned_to_email
        self.created_by = created_by
        self.status = status

        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d")
        if created == None:
            self.created = formatted_datetime
        else:
            self.created = created

    @classmethod
    def create_task(cls,task_name,due_date,assigned_to_email,created_by):
        if cls.task_exists(task_name, due_date):
            raise ValueError(f"A task with the name '{task_name}' and date '{due_date}' already exists.")

        new_task = cls(task_name, due_date, assigned_to_email,created_by)
        cls.save_task_to_file(new_task.__dict__)

    @classmethod
    def save_task_to_file(cls,task):
        try:
            with open(cls.FILE_PATH, 'a') as file:
                # Append the task data to the JSON file
                json.dump(task, file)
                file.write('\n')
            print("Task saved to file.")
        except Exception as e:
            print(f"Error saving task to file: {e}")

    @classmethod
    def task_exists(cls, task_name, due_date):
        try:
            with open(cls.FILE_PATH, 'r') as file:
                for line in file:
                    task_data = json.loads(line)
                    if task_data["task_name"] == task_name and task_data["due_date"] == due_date:
                        return True
            return False
        except Exception as e:
            print(f"Error reading tasks from file: {e}")
            return False
    
    @classmethod
    def get_task_by_name_and_date(cls, task_name, due_date):
        try:
            with open(cls.FILE_PATH, 'r') as file:
                for line in file:
                    task_data = json.loads(line)
                    if task_data["task_name"] == task_name and task_data["due_date"] == due_date:
                        return cls(**task_data)
            print(f"No task found with name '{task_name}' and date '{due_date}'.")
            return None
        except Exception as e:
            print(f"Error reading tasks from file: {e}")
            return None
        
    @classmethod
    def retrieve_task_per_assignee(cls, assignee_email):
        try:
            tasks_for_assignee = []
            with open(cls.FILE_PATH, 'r') as file:
                for line in file:
                    task_data = json.loads(line)
                    print(task_data)

                    if task_data["assigned_to_email"] == assignee_email:
                        tasks_for_assignee.append(cls(**task_data))
            return tasks_for_assignee
        except Exception as e:
            print(f"Error reading tasks from file: {e}")
            return []
        
    @classmethod
    def retrieve_task_per_creator(cls, creator_email):
        try:
            tasks_by_creator = []
            with open(cls.FILE_PATH, 'r') as file:
                for line in file:
                    task_data = json.loads(line)
                    if task_data["created_by"] == creator_email:
                        tasks_by_creator.append(cls(**task_data))
            return tasks_by_creator
        except Exception as e:
            print(f"Error reading tasks from file: {e}")
            return []

    @classmethod
    def update_task_status(cls, task_name, creator_email, new_status):
        try:
            with open(cls.FILE_PATH, 'r') as file:
                tasks = []
                for line in file:
                    task_data = json.loads(line)
                    if task_data["task_name"] == task_name and task_data["created_by"] == creator_email:
                        # Update the status of the matching task
                        task_data["status"] = new_status
                        print("Task updated.")
                    tasks.append(task_data)

            # Rewrite the entire file with updated tasks
            with open(cls.FILE_PATH, 'w') as file:
                for task in tasks:
                    json.dump(task, file)
                    file.write('\n')
        except Exception as e:
            print(f"Error updating task: {e}")

    @classmethod
    def update_task_teacher(cls, task_name_ilk, assigned_to_email, **kwargs):
        try:
            with open(cls.FILE_PATH, 'r') as file:
                tasks = []
                task_updated = False
                for line in file:
                    task_data = json.loads(line)
                    if task_data["task_name"] == task_name_ilk and task_data["assigned_to_email"] == assigned_to_email:
                        # Check if there are changes to be made
                        if any(task_data[key] != kwargs.get(key) for key in kwargs):
                            # Update the task based on provided keyword arguments
                            for key, value in kwargs.items():
                                task_data[key] = value
                                print(f"{key.capitalize()} updated by teacher to {value}")
                            task_updated = True
                    tasks.append(task_data)

            # Rewrite the entire file with updated tasks
            with open(cls.FILE_PATH, 'w') as file:
                for task in tasks:
                    json.dump(task, file)
                    file.write('\n')
            print("Task updated.")
            return task_updated
        except Exception as e:
            print(f"Error updating task: {e}")
            return False

    @classmethod
    def get_alternative_emails(cls):
        dummy_emails = ["assigned@example.com", "user2@example.com", "user3@example.com"]
        return dummy_emails
        





    