import sys, os
import uuid
sys.path.append(os.getcwd())
import json
import csv
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from db_connect import get_db_connection, retry_db_connection
import logging

class User():
    
    selected_user_ids = []
    
    logFile = 'data/logging.log'
    logFormat = '%(asctime)s - %(levelname)s - %(message)s'

    logging.basicConfig(filename=logFile, level=logging.DEBUG, format=logFormat)

    FILE_PATH = "data/users.txt"
    ANNOUNCEMENT_FILE_PATH = "data/announcements.txt"

    _current_user= None
    FILE_LESSON = "data/lessons.csv"
    FILE_MENTOR = "data/mentors.csv"
    FILE_ATT_LESSON = "data/lesson_attendance.csv"
    FILE_ATT_MENTOR = "data/mentor_attendance.csv"
    table_lesson = None
    table_mentoring = None
    table_student = None
    
    def __init__(self,user_id, name, surname, email, birthdate, city, phone_number, password, user_type,status, avatar_path,chat_status=None):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.email = email
        self.birthdate = birthdate
        self.city = city
        self.phone_number = phone_number
        self.password = password
        self.user_type = user_type
        self.status = status
        self.avatar_path = avatar_path
        self.chat_status = chat_status

    @classmethod
    def create_user(cls, name, last_name, email, birthdate, city, phone_number, password, user_type,status, avatar_path):
        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    if cls.email_exists(email):
                        QMessageBox.information(None, 'Warning', f'The email {email} already exists.', QMessageBox.Ok)
                   
                    else:
                        
                        #avatar_list=./sign/assets
                        #avatar_path=random.choice(avatar_list)
                        
                        query = """
                            INSERT INTO school.user (name, last_name, email, birthdate, city, phone_number, password_hash, user_type,status,avatar_path)
                            VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)
                            RETURNING user_id
                        """
                        cursor.execute(query, (name, last_name, email, birthdate, city, phone_number, password, user_type,status,avatar_path))
                        # Show a success message
                        conn.commit()
                        QMessageBox.information(None, 'Success', 'User created successfully.', QMessageBox.Ok)
                    
            except Exception as e:
                print(f"Error: {e}")
            
        
            
        
        
    @classmethod
    def email_exists(cls, email):
        existing_emails = cls.get_emails_for_task_assign()
        return email in existing_emails
    
    # @classmethod
    # def save_user(cls, user):
    #     try:
    #         with open(cls.FILE_PATH, 'a') as file:
    #             # Append the user data to the JSON file
    #             json.dump(user, file)
    #             file.write('\n')
    #         print("User saved to file.")
    #     except Exception as e:
    #         print(f"Error saving user to file: {e}")
    
    @classmethod
    def update_user_information(cls, email, **kwargs):
        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    # Update user information based on kwargs
                    update_query = "UPDATE school.user SET "
                    values = []
                    for key, value in kwargs.items():
                        update_query += f"{key} = %s, "
                        values.append(value)
                    update_query = update_query.rstrip(", ")  # Remove the trailing comma
                    update_query += " WHERE email = %s"
                    values.append(email)

                    cursor.execute(update_query, tuple(values))
                    conn.commit()
                    

                    #QMessageBox.information(None, 'Success', 'User information updated successfully.', QMessageBox.Ok)

            except Exception as e:
                print(f"Error updating user information: {e}")

    @classmethod
    def get_emails_for_task_assign(cls):
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)
        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    sql_query= """select 
                                user_id,
                                name,
                                last_name,
                                user_type,
                                avatar_path
                                FROM school.user
                                where user_type = 'student'
                                """
                    cursor.execute(sql_query)
                    result = cursor.fetchall() 
                    #print(result)
                    if result:
                        return result
                    else:
                        print("No user for task assign found.")
                        return []
            except Exception as e:
                print(f"Error: {e}")
                return None
            
    @classmethod
    def login(cls, email, password):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    query = '''
                    SELECT name, last_name, email, birthdate, city, phone_number, password_hash, user_type, status, avatar_path
                    FROM school.user
                    WHERE email = %s AND password_hash = %s
                    
                    '''
                    
                    cursor.execute(query, (email, password))
                    result = cursor.fetchone()
                    # Print the result for debugging
                    #print("Query Result:", result)
                    
                    if result:
                        user_data = {
                            "name": result[0],
                            "last_name": result[1],
                            "email": result[2],
                            "birthdate": result[3],
                            "city": result[4],
                            "phone_number": result[5],
                            "password_hash": result[6],
                            "user_type": result[7],
                            "status": result[8],
                            "avatar_path":result[9]
                        }
                        return user_data
        except Exception as e:
            print(f"Error reading user data from the database: {e}")
        return None

        

    @classmethod
    def set_currentuser(cls, email):
        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    sql_query = """
                    SELECT * FROM school."user" WHERE email = %s
                    """
                    cursor.execute(sql_query, (email,))
                    user_data = cursor.fetchone()
                    if user_data:
                        # Unpack the user_data tuple and create a User instance
                        user_instance = cls(*user_data)
                        cls._current_user = user_instance
                        return
            except Exception as e:
                print(f"Error setting current user: {e}")
                
   
                
    @classmethod
    def get_teachers_by_status(cls, status):
        teachers = []
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    sql_query = '''
                    SELECT name, email, status
                    FROM school.user
                    WHERE user_type = 'teacher' AND status = %s
                    '''
                    cursor.execute(sql_query, (status,))
                    teachers = cursor.fetchall()

        except Exception as e:
            print(f"Error getting teachers by status: {e}")
            
        teachers_with_options = [(name, email, status, 'Approve', 'Reject') for name, email, status in teachers]
        return teachers
                
    #---------------------------------------------------------------------------------------

    @classmethod
    def get_count_message_for_group(cls,group_id):
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    sql_query = """
                        SELECT COUNT(*)
                        FROM school.chat
                        WHERE group_id = %s
                    """
                    cursor.execute(sql_query, (group_id,))
                    result = cursor.fetchone() 
                    #print(result)
                    if result:
                        count = result[0]
                        #print(f"Current message count in group is {count}")
                        return count
                    else:
                        print("No result found.")
                        return None
            except Exception as e:
                print(f"Error: {e}")
                return None

    @classmethod
    def get_other_user_typing_status(cls,group_id,user_id):
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    sql_query = """
                        SELECT
                            u.name
                        FROM
                            school.chat_user AS cu
                        LEFT JOIN
                            school.user AS u ON cu.member_id = u.user_id
                        WHERE
                            cu.group_id = %s AND cu.typing_status = 'typing' AND cu.member_id != %s;
                    """
                    cursor.execute(sql_query, (group_id,user_id))
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
    def get_typing_count(cls,group_id,user_id):
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    sql_query = """
                        SELECT COUNT(*)
                        FROM school.chat_user
                        WHERE group_id = %s and typing_status = 'typing' and member_id != %s
                    """
                    cursor.execute(sql_query, (group_id,user_id))
                    result = cursor.fetchone() 
                    #print(result)
                    if result:
                        count = result[0]
                        #print(f"Current message count in group is {count}")
                        return count
                    else:
                        print("No result found.")
                        return None
            except Exception as e:
                print(f"Error: {e}")
                return None



    @classmethod
    def update_user_last_seen(cls,user_id, status):
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    sql_query = """
                        UPDATE school.user
                        SET chat_status = %s
                        WHERE user_id = %s
                    """
                    cursor.execute(sql_query, (status,user_id))
                    conn.commit()
                    print(f"User {user_id} status is updated to {status}")
            except Exception as e:
                print(f"Error: {e}")
                return None


    @classmethod
    def check_group_id_of_users(cls,active_user_id, other_user_id):
        #user_id, user_type, group_id, name, last_name, avatar_path = user
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    sql_query = """
                        SELECT group_id
                        FROM school.chat_user
                        GROUP BY group_id
                        HAVING COUNT(DISTINCT CASE WHEN member_id IN (%s, %s) THEN member_id END) = 2
                        AND COUNT(*) = 2;
                    """
                    cursor.execute(sql_query, (active_user_id,other_user_id))
                    result = cursor.fetchall()
                    #print(result)
                    return result
            except Exception as e:
                print(f"Error: {e}")
                return None
            
    @classmethod
    def update_user_status(cls, group_id, member_id,status):
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    sql_query = """
                        UPDATE school.chat_user
                        SET typing_status = %s 
                        WHERE group_id = %s AND member_id = %s
                    """
                    cursor.execute(sql_query, (status, group_id, member_id))
                    conn.commit()
                    #print("typing status is updated in database")
            except Exception as e:
                print(f"Error: {e}")
                return None

    @classmethod
    def insert_message_read(cls,user_id,message_id_list):
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    sql_query = """
                        UPDATE school.chat_status 
                        SET is_read = %s 
                        WHERE message_id = %s AND member_id = %s
                    """

                    for message_id in message_id_list:
                        cursor.execute(sql_query, (True,message_id,user_id))

                    conn.commit()
                    return {"Successful to insert is read for user message"}
            except Exception as e:
                print(f"Error: {e}")
                return None


    @classmethod
    def update_chat_status(cls,current_user_id,group_id,member_list):
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    sql_query = """
                        INSERT INTO school.chat_status (group_id, member_id, is_read)
                        VALUES (%s, %s, %s)
                    """
                    for member_id in member_list:
                        is_read = member_id == current_user_id
                        cursor.execute(sql_query, (group_id,member_id,is_read))
                        #print(result)
                    conn.commit()
            except Exception as e:
                print(f"Error: {e}")
                return None

    @classmethod
    def get_users_for_search_to_message(cls,user_id):
        #user_id, user_type, group_id, name, last_name, avatar_path = user
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    sql_query = """
                        SELECT 
                            u.user_id,
                            u.name,
                            u.last_name,
                            u.user_type,
                            u.avatar_path
                        FROM 
                            school.user AS u
                        WHERE 
                            u.user_id != %s AND u.status = 'active';
                    """
                    cursor.execute(sql_query, (user_id,))
                    result = cursor.fetchall()
                    #print(result)
                    return result
            except Exception as e:
                print(f"Error: {e}")
                return None

    @classmethod
    def get_users_for_group_create(cls, user_id):
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    sql_query = """
                        SELECT * FROM school.user WHERE user_id != %s and status = 'active'
                    """
                    cursor.execute(sql_query, (user_id,))
                    result = cursor.fetchall()
                    #print(result)
                    return result
            except Exception as e:
                print(f"Error: {e}")
                return None

    @classmethod
    def send_message(cls,sender_id,group_id,message,member_list):
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    data_to_insert = {
                        'sender_id': sender_id,
                        'group_id' : group_id,
                        'message' : message
                    }

                    insert_query = """
                        INSERT INTO school.chat ({columns})
                        VALUES ({values})
                        RETURNING message_id
                    """.format(
                        columns=', '.join(data_to_insert.keys()),
                        values=', '.join(['%s' for _ in data_to_insert.values()])
                    )
                    cursor.execute(insert_query, tuple(data_to_insert.values()))
                    inserted_pk = cursor.fetchone()[0]
                    print(f"new message is created with id: {inserted_pk}")
                    if inserted_pk is not None:
                        insert_chat_status_query = """
                            INSERT INTO school.chat_status (message_id, member_id, is_read)
                            VALUES (%s, %s, %s)
                        """
                        for member_id in member_list:
                            is_read = member_id == sender_id
                            cursor.execute(insert_chat_status_query, (inserted_pk,member_id,is_read))
                            #print(result)
                    else: 
                        return {"Error inserting the message, so that chat_status is not inserted"}

                    conn.commit()

                    return inserted_pk
            except Exception as e:
                print(f"Error: {e}")
                conn.rollback()
                return None
    @classmethod
    def create_message_group(cls, group_name, member_list):
        # Generate a common UUID for all members
        common_uuid = str(uuid.uuid4())

        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    # Insert records for each member
                    for member_id in member_list:
                        sql_query = """
                            INSERT INTO school.chat_user (group_id, member_id, group_name)
                            VALUES (%s, %s, %s);
                        """
                        cursor.execute(sql_query, (common_uuid, member_id, group_name))
                    conn.commit()
                    return common_uuid
            except Exception as e:
                print(f"Error: {e}")
                conn.rollback()

    @classmethod
    def get_latest_messages_for_member(cls, user_id):
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    sql_query = """
                        WITH GroupsWithMember1 AS (
                            SELECT DISTINCT group_id
                            FROM school.chat_user
                            WHERE member_id = %s
                        ),
                        FirstNonMember1InEachGroup AS (
                            SELECT DISTINCT ON (cu.group_id) cu.*
                            FROM school.chat_user cu
                            JOIN GroupsWithMember1 gwm1 ON cu.group_id = gwm1.group_id
                            WHERE cu.member_id <> %s
                            ORDER BY cu.group_id, cu.member_id
                        )
                        -- Retrieve the latest message in each group with member_id, group_name, and user name
                        SELECT
                            gwm1.group_id,
                            fm1.message_id,
                            fm1.sender_id,
                            fm1.message,
                            fm1.created_datetime,
                            fnm1.member_id,
                            fnm1.group_name,
                            u.name AS user_name,
                            u.avatar_path as avatar_path
                        FROM GroupsWithMember1 gwm1
                        LEFT JOIN (
                            SELECT
                                c.group_id,
                                c.message_id,
                                c.sender_id,
                                c.message,
                                c.created_datetime,
                                ROW_NUMBER() OVER (PARTITION BY c.group_id ORDER BY c.created_datetime DESC) AS message_rank
                            FROM school.chat c
                        ) AS fm1 ON gwm1.group_id = fm1.group_id
                        JOIN FirstNonMember1InEachGroup fnm1 ON gwm1.group_id = fnm1.group_id
                        JOIN school."user" u ON fnm1.member_id = u.user_id
                        WHERE fm1.message_rank = 1 OR fm1.message_id IS NULL
                        ORDER BY gwm1.group_id;
                    """
                    cursor.execute(sql_query, (user_id,user_id))
                    active_messages = cursor.fetchall()

                    if active_messages is not None:
                        groups = [item[0] for item in active_messages]
                        unread_count_query = """
                            SELECT 
                                c.group_id,
                                COUNT(*) AS unread_count
                            FROM
                                school.chat AS c
                            LEFT JOIN
                                school.chat_status AS cs ON c.message_id = cs.message_id
                            WHERE
                                c.group_id IN %s
                                AND (cs.is_read IS NULL OR cs.is_read = FALSE)
                                AND cs.member_id = %s
                            GROUP BY c.group_id;
                        """
                        cursor.execute(unread_count_query, (tuple(groups),user_id))
                        
                        unread_count_result = cursor.fetchall()

                        # Create a dictionary to map group_id to unread_count
                        unread_count_dict = {group_id: unread_count for group_id, unread_count in unread_count_result}
                        

                        # Append unread_count to each item in active_messages
                        result = [
                            (
                                group_id,
                                message_id,
                                sender_id,
                                message,
                                created_datetime,
                                member_id,
                                group_name,
                                user_name,
                                avatar_path,
                                unread_count_dict.get(group_id, 0)
                            )
                            for group_id, message_id, sender_id, message, created_datetime, member_id, group_name, user_name, avatar_path in active_messages
                        ]
                        return result
                    else:
                        return None
            except Exception as e:
                print(f"Error: {e}")
                return None
            
    @classmethod
    def check_read_status_for_unread_messages(cls,unread_message_list):
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None or unread_message_list == []:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    message_read_query =""" SELECT
                                                message_id
                                            FROM
                                                school.chat_status
                                            WHERE
                                                message_id IN %s
                                            GROUP BY
                                                message_id
                                            HAVING
                                                COUNT(*) = SUM(CASE WHEN is_read THEN 1 ELSE 0 END);"""

                    cursor.execute(message_read_query, (tuple(unread_message_list),))
                    message_read_statuses = cursor.fetchall()
                    if not message_read_statuses:
                        return None
                    else:
                        return message_read_statuses
            except Exception as e:
                print(f"Error: {e}")
                return None

    @classmethod
    def get_message_user_info(cls,group_id,member_id):
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    group_query =   """ select 
                                        cu.id,
                                        cu.member_id,
                                        cu.group_name,
                                        u.name,
                                        u.last_name,
                                        u.user_type,
                                        u.avatar_path,
                                        u.chat_status
                                        from school.chat_user cu 
                                        left join school."user" u on cu.member_id = u.user_id
                                        where group_id = %s and member_id != %s"""

                    cursor.execute(group_query, (group_id,member_id))
                    group_info = cursor.fetchall()
                    return group_info
            except Exception as e:
                print(f"Error: {e}")
                return None
            
            
    @classmethod
    def get_specific_communication(cls,group_id,member_id):
        print(f"requested group_id for message is = {group_id}")
        connection = retry_db_connection(get_db_connection, max_retries=3, retry_delay=5)

        if connection is None:
            return None

        with connection as conn:
            try:
                with conn.cursor() as cursor:
                    message_query = """
                    SELECT
                        c.message_id,
                        c.sender_id,
                        c.group_id,
                        c.message,
                        c.created_datetime,
                        u."name",
                        u.last_name,
                        u.user_type,
                        u.avatar_path,
                        cs.is_read,
                        CASE 
                            WHEN cs.is_read IS NULL THEN FALSE
                            WHEN (
                                SELECT COUNT(DISTINCT member_id)
                                FROM school.chat_status
                                WHERE message_id = c.message_id AND is_read = true
                            ) = (
                                SELECT COUNT(DISTINCT member_id)
                                FROM school.chat_status
                                WHERE message_id = c.message_id
                            ) THEN true 
                            ELSE false 
                        END AS group_read
                    FROM school.chat c
                    LEFT JOIN school."user" u ON c.sender_id = u.user_id
                    LEFT JOIN school.chat_status cs ON c.message_id = cs.message_id AND cs.member_id = %s
                    WHERE c.group_id = %s
                    ORDER BY c.created_datetime ASC
                    """

                    cursor.execute(message_query, (member_id,group_id,))
                    messages = cursor.fetchall()
                    #print(messages)
                    return messages
            except Exception as e:
                print(f"Error: {e}")
                return None

# Save the user information to the file
# User.create_user(
#     name="Student",
#     surname="Test",
#     email="student@example.com",
#     birthdate="1990-01-01",
#     city="Ist",
#     phone_number="123-456-7890",
#     password="12345",
#     user_type="student"
# )
    
    @classmethod
    def create_lessons(cls, email, lesson_info):
        try:
            date, lesson, start, finish = lesson_info

            with get_db_connection() as conn:
                try:
                    with conn.cursor() as cursor:
                        
                        cursor.execute("SELECT user_id FROM school.user WHERE email = %s", (email,))
                        user_id = cursor.fetchone()[0]

                        
                        cursor.execute('''
                            INSERT INTO school.mentoringlesson (name, date, start, finish, type, user_id)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        ''', (lesson, date, start, finish, 'lesson', user_id))

                        logging.info(f"Lesson created successfully by email {email}: {lesson_info}")            
                except Exception as e:
                    print(f"Error in create lesson: {e}")

        except Exception as e:
            print(f"Error in create lesson: {e}")


    @classmethod
    def get_LessonSchedule(cls):

        if cls.table_lesson is None: 
            cls.table_lesson = QTableWidget()
            cls.table_lesson.setColumnCount(4)

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT name, date, start, finish FROM school.mentoringlesson WHERE type = 'lesson'")
                    lessons = cursor.fetchall()

                    cls.table_lesson.setRowCount(0)

                    for row_number, lesson in enumerate(lessons):
                        cls.table_lesson.insertRow(row_number)
                        for column_number, info in enumerate(lesson):
                            cls.table_lesson.setItem(row_number, column_number, QTableWidgetItem(str(info)))

            except Exception as e:
                print(f"Error: {e}")

        return cls.table_lesson
    
    @classmethod
    def get_Lesson_Attendance(cls):
        if cls.table_lesson is None: 
            cls.table_lesson = QTableWidget()
            cls.table_lesson.setColumnCount(2) 

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT name FROM school.mentoringlesson WHERE type = 'lesson'") 
                    lessons = cursor.fetchall()
                    cls.table_lesson.setRowCount(0)

                    for row_number, lesson in enumerate(lessons):
                        cls.table_lesson.insertRow(row_number)
                        for column_number, info in enumerate(lesson):
                            cls.table_lesson.setItem(row_number, column_number, QTableWidgetItem(str(info)))

                        list_button = QPushButton("List")
                        list_button.clicked.connect(lambda _, lesson_name=lesson[0]: cls.open_students_page_lesson(lesson_name))
                        cls.table_lesson.setCellWidget(row_number, 2, list_button)
            
            except Exception as e:
                print(f"Error in getting lesson: {e}")

        return cls.table_lesson
    
    @classmethod
    def get_Lesson_Attendance_Student(cls, email):
        if cls.table_lesson is None:
            cls.table_lesson = QTableWidget()
            cls.table_lesson.setColumnCount(4)

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute('''
                        SELECT us.name, us.last_name, att.status, ml.name 
                        FROM school.user AS us
                        JOIN school.attendance AS att ON us.user_id = att.user_id
                        JOIN school.mentoringlesson AS ml ON att.mentoringlesson_id = ml.id
                        WHERE ml.type = 'lesson' AND us.email = %s
                    ''', (email,))
                    lessons = cursor.fetchall()

                    cls.table_lesson.setRowCount(0)

                    for row_number, lesson in enumerate(lessons):
                        cls.table_lesson.insertRow(row_number)
                        for column_number, info in enumerate(lesson):
                            cls.table_lesson.setItem(row_number, column_number, QTableWidgetItem(str(info)))

            except Exception as e:
                print(f"Error: {e}")

        return cls.table_lesson
    
    @classmethod
    def get_Mentor_Attendance_Student(cls, email):
        if cls.table_mentoring is None:
            cls.table_mentoring = QTableWidget()
            cls.table_mentoring.setColumnCount(4)
        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute('''
                        SELECT us.name, us.last_name, att.status, ml.name 
                        FROM school.user AS us
                        JOIN school.attendance AS att ON us.user_id = att.user_id
                        JOIN school.mentoringlesson AS ml ON att.mentoringlesson_id = ml.id
                        WHERE ml.type = 'mentor' AND us.email = %s
                    ''', (email,))
                    mentors = cursor.fetchall()

                    cls.table_mentoring.setRowCount(0)

                    for row_number, mentor in enumerate(mentors):
                        cls.table_mentoring.insertRow(row_number)
                        for column_number, info in enumerate(mentor):
                            cls.table_mentoring.setItem(row_number, column_number, QTableWidgetItem(str(info)))

            except Exception as e:
                print(f"Error: {e}")
        return cls.table_mentoring
    
    @classmethod
    def get_Mentor_Attendance(cls):
        if cls.table_mentoring is None: 
            cls.table_mentoring = QTableWidget()
            cls.table_mentoring.setColumnCount(2) 

        try:
            with open(cls.FILE_MENTOR, 'r', newline='') as file:
                reader = csv.reader(file)
                cls.table_mentoring.setRowCount(0)
                row_number = 0

                for row in reader:
                    if len(row) > 1:
                        cls.table_mentoring.insertRow(row_number)
                        mentor_name = row[1]
                        cls.table_mentoring.setItem(row_number, 0, QTableWidgetItem(mentor_name)) 
                        button = QPushButton("List")
                        button.clicked.connect(lambda _, mentor=mentor_name: cls.open_students_page_mentor(mentor))
                        cls.table_mentoring.setCellWidget(row_number, 1, button) 
                        row_number += 1
            
        except Exception as e:
            print(f"Error in getting lesson: {e}")

        return cls.table_mentoring
    
    @classmethod
    def open_students_page_lesson(cls, item):
        selected_lesson = item
        students = cls.get_students()
        if students:
            cls.students_window = QWidget()
            cls.students_table = QTableWidget()
            cls.students_table.setColumnCount(4)
            cls.students_table.setRowCount(len(students))
            header = ["E-Mail","Name", "Surname", "Attendance"]
            cls.students_table.setHorizontalHeaderLabels(header)
            for i, column_name in enumerate(header):
                cls.students_table.setColumnWidth(i, 220)
            for row, (email, name, surname) in enumerate(students):
                cls.students_table.setRowHeight(row, 50)
            for row, (email, name, surname) in enumerate(students):
                cls.students_table.setItem(row, 0, QTableWidgetItem(email))
                cls.students_table.setItem(row, 1, QTableWidgetItem(name))
                cls.students_table.setItem(row, 2, QTableWidgetItem(surname))
                attended_btn = QPushButton("Attended")
                attended_btn.clicked.connect(lambda _, r=row: cls.mark_attendance_lesson(selected_lesson, r, "Attended"))
                attended_btn.setFixedWidth(100)
                not_attended_btn = QPushButton("Not Attended")
                not_attended_btn.clicked.connect(lambda _, r=row: cls.mark_attendance_lesson(selected_lesson, r, "Not Attended"))
                not_attended_btn.setFixedWidth(100)
                buttons_layout = QHBoxLayout()
                buttons_layout.addWidget(attended_btn)
                buttons_layout.addWidget(not_attended_btn)
                widget = QWidget()
                widget.setLayout(buttons_layout)
                cls.students_table.setCellWidget(row, 3, widget)
            layout = QVBoxLayout()
            layout.addWidget(cls.students_table)
            cls.students_window.setLayout(layout)
            cls.students_window.setWindowTitle(f"Students in {selected_lesson}")
            cls.students_window.show()
        else:
            QMessageBox.warning(cls, "No Students", "There are no students for this lesson.")


    @classmethod
    def mark_attendance_lesson(cls, lesson_name, row, attendance_status):

        btn_widget = cls.students_table.cellWidget(row, 3)
        attended_btn = btn_widget.layout().itemAt(0).widget()
        not_attended_btn = btn_widget.layout().itemAt(1).widget()
        attended_btn.setEnabled(False)
        not_attended_btn.setEnabled(False)

        student_email = cls.students_table.item(row, 0).text()

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT user_id FROM school.user WHERE email = %s", (student_email,))
                    user_id = cursor.fetchone()[0]
                    cursor.execute("SELECT id FROM school.mentoringlesson WHERE name = %s", (lesson_name,))
                    lesson_id = cursor.fetchone()[0]
                    cursor.execute('''
                        INSERT INTO school.attendance (mentoringlesson_id, user_id, status)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (mentoringlesson_id, user_id) DO UPDATE SET status = %s
                    ''', (lesson_id, user_id, attendance_status))

            except Exception as e:
                print(f"Error in marking attendance: {e}")
    
    
    @classmethod
    def open_students_page_mentor(cls, item):
        selected_mentor = item
        students = cls.get_students()
        if students:
            cls.students_window = QWidget()
            cls.students_table = QTableWidget()
            cls.students_table.setColumnCount(4)
            cls.students_table.setRowCount(len(students))
            header = ["E-Mail","Name", "Surname", "Attendance"]
            cls.students_table.setHorizontalHeaderLabels(header)
            for i, column_name in enumerate(header):
                cls.students_table.setColumnWidth(i, 220)
            for row, (email, name, surname) in enumerate(students):
                cls.students_table.setRowHeight(row, 50)
            for row, (email, name, surname) in enumerate(students):
                cls.students_table.setItem(row, 0, QTableWidgetItem(email))
                cls.students_table.setItem(row, 1, QTableWidgetItem(name))
                cls.students_table.setItem(row, 2, QTableWidgetItem(surname))
                attended_btn = QPushButton("Attended")
                attended_btn.clicked.connect(lambda _, r=row: cls.mark_attendance_mentor(selected_mentor, r, "Attended"))
                attended_btn.setFixedWidth(100)
                not_attended_btn = QPushButton("Not Attended")
                not_attended_btn.clicked.connect(lambda _, r=row: cls.mark_attendance_mentor(selected_mentor, r, "Not Attended"))
                not_attended_btn.setFixedWidth(100)
                buttons_layout = QHBoxLayout()
                buttons_layout.addWidget(attended_btn)
                buttons_layout.addWidget(not_attended_btn)
                widget = QWidget()
                widget.setLayout(buttons_layout)
                cls.students_table.setCellWidget(row, 3, widget)
            layout = QVBoxLayout()
            layout.addWidget(cls.students_table)
            cls.students_window.setLayout(layout)
            cls.students_window.setWindowTitle(f"Students in {selected_mentor}")
            cls.students_window.show()
        else:
            QMessageBox.warning(cls, "No Students", "There are no students for this lesson.")

    @classmethod
    def mark_attendance_mentor(cls, mentor_name, row, attendance_status):
       
        btn_widget = cls.students_table.cellWidget(row, 3)
        attended_btn = btn_widget.layout().itemAt(0).widget()
        not_attended_btn = btn_widget.layout().itemAt(1).widget()
        attended_btn.setEnabled(False)
        not_attended_btn.setEnabled(False)

        student_email = cls.students_table.item(row, 0).text()

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT user_id FROM school.user WHERE email = %s", (student_email,))
                    user_id = cursor.fetchone()[0]
                    cursor.execute("SELECT id FROM school.mentoringlesson WHERE name = %s", (mentor_name,))
                    mentor_id = cursor.fetchone()[0]
                    cursor.execute('''
                        INSERT INTO school.attendance (mentoringlesson_id, user_id, status)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (mentoringlesson_id, user_id) DO UPDATE SET status = %s
                    ''', (mentor_id, user_id, attendance_status))

            except Exception as e:
                print(f"Error in marking attendance: {e}")

    @classmethod
    def get_students(cls):
        students = []

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT email, name, last_name FROM school.user WHERE user_type = 'student'")
                    student_records = cursor.fetchall()

                    for record in student_records:
                        email, name, surname = record
                        students.append((email, name, surname))

            except Exception as e:
                print(f"Error in getting students: {e}")

        return students
    
    @classmethod
    def get_lesson_names(cls):
        lesson_names = []

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT name FROM school.mentoringlesson WHERE type = 'lesson'")
                    lessons = cursor.fetchall()

                    for lesson in lessons:
                        lesson_names.append(lesson[0])

            except Exception as e:
                print(f"Error in getting lesson names: {e}")

        return lesson_names
    
    @classmethod
    def get_lesson_names(cls):
        mentor_names = []

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT name FROM school.mentoringlesson WHERE type = 'mentor'")
                    mentors = cursor.fetchall()

                    for mentor in mentors:
                        mentor_names.append(mentor[0])

            except Exception as e:
                print(f"Error in getting mentor names: {e}")

        return mentor_names

    @classmethod
    def create_mentor(cls, email, mentor_info):
        try:
            date, mentor, start, finish = mentor_info

            with get_db_connection() as conn:
                try:
                    with conn.cursor() as cursor:
                        
                        cursor.execute("SELECT user_id FROM school.user WHERE email = %s", (email,))
                        user_id = cursor.fetchone()[0]

                        
                        cursor.execute('''
                            INSERT INTO school.mentoringlesson (name, date, start, finish, type, user_id)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        ''', (mentor, date, start, finish, 'mentor', user_id))

                        logging.info(f"Mentor created successfully by {email}: {mentor_info}")            
                except Exception as e:
                    print(f"Error in create mentor: {e}")

        except Exception as e:
            print(f"Error in create mentor: {e}")

    
    @classmethod
    def get_Mentor_Schedule(cls):
        if cls.table_mentoring is None: 
            cls.table_mentoring = QTableWidget()
            cls.table_mentoring.setColumnCount(4)

        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT name, date, start, finish FROM school.mentoringlesson WHERE type = 'mentor'")
                    mentors = cursor.fetchall()

                    cls.table_mentoring.setRowCount(0)

                    for row_number, lesson in enumerate(mentors):
                        cls.table_mentoring.insertRow(row_number)
                        for column_number, info in enumerate(lesson):
                            cls.table_mentoring.setItem(row_number, column_number, QTableWidgetItem(str(info)))

            except Exception as e:
                print(f"Error: {e}")

        return cls.table_mentoring
    
    # @classmethod
    # def get_announcements(cls):
    #     announcements = []
    #     try:
    #         with open(cls.ANNOUNCEMENT_FILE_PATH, 'r') as file:
    #             for line in file:
    #                 announcement_data = json.loads(line)
    #                 announcements.append(announcement_data)
    #         sorted_announcements = sorted(announcements, key=lambda x: x.get("timestamp"), reverse=True)

    #     except Exception as e:
    #         print(f"Error reading announcements from file: {e}")
    #     return sorted_announcements
    @classmethod
    def get_announcements(cls):
        announcements = []
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    query = '''
                        SELECT u.name, d.expression, d.expiry_date
                        FROM school.duyuru as d
                        LEFT JOIN school.user as u ON d.user_id = u.user_id
                        ORDER BY expiry_date DESC
                    '''
                    cursor.execute(query)
                    result = cursor.fetchall()

                    for row in result:
                        announcement_data = {
                            "user_id": row[0],
                            "announcement": row[1],
                            "expiry_date": QDateTime.fromString(row[2], Qt.ISODate).toString(Qt.ISODate),  
                            #"due_date":row[3].isoformat()
                        }
                        announcements.append(announcement_data)

        except Exception as e:
            print(f"Error reading announcements from database: {e}")

        return announcements
    
    # @classmethod
    # def get_announcements_to_delete(cls, email, user_type):
    #     announcements = []
    #     try:
    #         with open(cls.ANNOUNCEMENT_FILE_PATH, 'r') as file:
    #             for line in file:
    #                 announcement_data = json.loads(line)
    #                 created_by = announcement_data.get('created_by')
    #                 # Check user type and email conditions
    #                 if (user_type == "admin") or (user_type == "teacher" and created_by == email):
    #                     announcements.append(announcement_data)
    #     except Exception as e:
    #         print(f"Error reading announcements from file: {e}")
    #     return announcements
    @classmethod
    def get_announcements_to_delete(cls, email, user_type):
        announcements = []
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # Find user_id associated with the given email
                    user_query = "SELECT user_id FROM school.user WHERE email = %s"
                    cursor.execute(user_query, (email,))
                    user_id = cursor.fetchone()[0] if email else None
                    query = '''
                        SELECT user_id, expression, expiry_date
                        FROM school.duyuru
                    '''
                    cursor.execute(query)
                    result = cursor.fetchall()

                    for row in result:
                        announcement_data = {
                            "user_id": row[0],
                            "announcement": row[1],
                            "expiry_date": QDateTime.fromString(row[2], Qt.ISODate).toString(Qt.ISODate),
                            #"due_date": row[3].isoformat()
                        }
                        # Check user type and email conditions
                        if (user_type == "admin") or (user_type == "teacher" and announcement_data["user_id"] == user_id):
                            announcements.append(announcement_data)

        except Exception as e:
            print(f"Error reading announcements from database: {e}")

        return announcements

    
    # @classmethod
    # def delete_announcement(cls, text):
    #     try:
    #         # Read existing announcements
    #         with open(cls.ANNOUNCEMENT_FILE_PATH, 'r') as file:
    #             announcements = [json.loads(line) for line in file]

    #         # Find and remove the announcement based on the name
    #         updated_announcements = [announcement for announcement in announcements
    #                                 if announcement.get('announcement') != text]

    #         # Write the updated announcements back to the file
    #         with open(cls.ANNOUNCEMENT_FILE_PATH, 'w') as file:
    #             for announcement in updated_announcements:
    #                 json.dump(announcement, file)
    #                 file.write('\n')

    #         print(f"Announcement '{text}' deleted.")
    #     except Exception as e:
    #         print(f"Error deleting announcement: {e}")
    @classmethod
    def delete_announcement(cls, text):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # Delete announcement from the database
                    query = '''
                        DELETE FROM school.duyuru
                        WHERE expression = %s
                    '''
                    cursor.execute(query, (text,))
                    conn.commit()
                    #Add log file
                    logging.info(f"Announcement  deleted successfully by {User._current_user.name}")

            print(f"Announcement '{text}' deleted from the database ")
        except Exception as e:
            print(f"Error deleting announcement: {e}")


    # @classmethod
    # def create_announcement(cls, announcement, created_by):
    #     try:
    #         # Read existing announcements
    #         with open(cls.ANNOUNCEMENT_FILE_PATH, 'r') as file:
    #             existing_announcements = [json.loads(line) for line in file]

    #         # Check if the announcement with the same name already exists
    #         if any(existing_announcement['announcement'] == announcement for existing_announcement in existing_announcements):
    #             return False, "Error: Announcement with the same name already exists."

    #         # Append the announcement data to the JSON file
    #         with open(cls.ANNOUNCEMENT_FILE_PATH, 'a') as file:
    #             announcement_data = {
    #                 'announcement': announcement,
    #                 'created_by': created_by,
    #                 'timestamp': QDateTime.currentDateTime().toString(Qt.ISODate)
    #             }
    #             json.dump(announcement_data, file)
    #             file.write('\n')
            
    #         return True, "Announcement created"
    #     except Exception as e:
    #         print(f"Error creating announcement: {e}")
    
    @classmethod
    def create_announcement(cls, announcement, created_by):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    user_query = "SELECT user_id FROM school.user WHERE email = %s"
                    cursor.execute(user_query, (cls._current_user.email,))
                    user_id = cursor.fetchone()[0] if cls._current_user else None
                    # Insert announcement into the database
                    query = f'''
                        INSERT INTO school.duyuru
                        (user_id, expression, expiry_date) 
                        VALUES (%s, %s, %s)
                    '''
                    expiry_date = QDateTime.currentDateTime().toString(Qt.ISODate)
                    cursor.execute(query, (user_id, announcement,  expiry_date))
                    conn.commit()
                    #Add log file
                    logging.info(f"Announcement  created successfully by {User._current_user.name} ")

            return True, "Announcement created"
            
        except Exception as e:
            print(f"Error creating announcement: {e}")
            return False, f"Error creating announcement: {e}"






