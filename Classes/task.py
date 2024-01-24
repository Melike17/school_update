from datetime import datetime
import json
from db_connect import get_db_connection, retry_db_connection

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
    def create_task(cls,user_id,task_name,due_date,assignees):
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    insert_task = """INSERT INTO school.task
                                (expression,createdby,duedate,created_at)
                                VALUES
                                (%s,%s,%s,%s)
                                RETURNING task_id
                                """
                    current_datetime = datetime.now()
                    formatted_datetime = current_datetime.strftime("%Y-%m-%d")
                    cursor.execute(insert_task, (task_name,int(user_id), due_date,formatted_datetime ))
                    task_id = cursor.fetchone()[0]

                    insert_relation = """INSERT INTO school.task_user
                                (user_id,task_id,status)
                                VALUES
                                (%s,%s,%s)
                                """
                    for user in assignees:
                        cursor.execute(insert_relation, (user, task_id, "In Progress"))
                    conn.commit()
            except Exception as e:
                print(f"Error: {e}")
                return None
        

        

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
    def retrieve_task_per_creator(cls, user_id):
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    sql_query = """SELECT
                                    t.task_id,
                                    t.expression,
                                    t.duedate,
                                    t.created_at,
                                    jsonb_agg(jsonb_build_object('user_id', u.user_id, 'status', tu.status, 'name', u.name, 'last_name', u.last_name, 'email', u.email, 'avatar', u.avatar_path)) AS user_info
                                FROM
                                    school.task AS t
                                LEFT JOIN
                                    school.task_user AS tu ON t.task_id = tu.task_id
                                LEFT JOIN
                                    school.user AS u ON tu.user_id = u.user_id
                                WHERE t.createdby = %s
                                GROUP BY
                                    t.task_id;    
                            """
                    cursor.execute(sql_query, (user_id,))
                    result = cursor.fetchall() 
                    #print(result)
                    if result:
                        return result
                    else:
                        print("No typing user found.")
                        return []
            except Exception as e:
                print(f"Error: {e}")
                return None
            
    @classmethod
    def retrieve_student_tasks(cls, user_id):
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    sql_query = """select 
                                    tu.task_id,
                                    tu.user_id,
                                    tu.status,
                                    t.expression,
                                    t.duedate,
                                    t.created_at,
                                    t.createdby,
                                    u.name,
                                    u.last_name,
                                    u.avatar_path
                                    from school.task_user as tu
                                    left join school.task as t ON tu.task_id = t.task_id
                                    left join school.user as u ON t.createdby = u.user_id
                                    where tu.user_id = %s 
                            """
                    cursor.execute(sql_query, (int(user_id),))
                    result = cursor.fetchall() 
                    #print(result)
                    if result:
                        return result
                    else:
                        print("No typing user found.")
                        return []
            except Exception as e:
                print(f"Error: {e}")
                return None
        
        

    @classmethod
    def update_task_status(cls, user_id, task_list, new_status):
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    update_status = """UPDATE school.task_user
                                    SET status = %s
                                    WHERE user_id = %s AND task_id = %s;
                                """
                    for task_id in task_list:
                        cursor.execute(update_status, (new_status, user_id, task_id))
                    conn.commit()
            except Exception as e:
                print(f"Error: {e}")
                return None

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
        




