import sys, os
sys.path.append(os.getcwd())

import csv
import os
import ast
from datetime import datetime

import json
import psycopg2
import uuid
from db_connect import get_db_connection



class Chat():
    FILE_PATH = "data/chat.txt"
    
    # PostgreSQL bağlantısını sınıf düzeyinde tanımlayın
    conn = psycopg2.connect("postgres://wqkprbpj:75qiQUbf9e5JKKz4P_HxTbD2aViCmxl4@snuffleupagus.db.elephantsql.com/wqkprbpj")

    def __init__(self, message_id, sender_user_id, created_datetime,receiver_name, message_text ):
        self.message_id = message_id
        self.sender_user_id = sender_user_id
        self.created_datetime = created_datetime
        self.receiver_name = receiver_name
        self.message_text= message_text
       
        # created_datetime'i string formatına çevir
        datetime_str = ast.literal_eval(created_datetime)
        # string formatındaki tarihi datetime nesnesine dönüştür
        self.created_datetime = datetime.strptime(datetime_str, "datetime.datetime(%Y, %m, %d, %H, %M, %S, %f)")

        # created_datetime'i ayrıştır ve tarih ile saat olarak ayır
        self.date = self.created_datetime.date()
        self.time = self.created_datetime.time()
    @classmethod
    def create_chat(cls):
        # PostgreSQL connection
        cursor = cls.conn.cursor()
        
        # Insert the message into the 'chat' table
        #insert_query = "INSERT INTO chat (message_id, sender_name, avatar_link, message, date, time) VALUES (%s, %s, %s, %s, %s, %s)"
        #cursor.execute(insert_query, (message_id, sender_name, avatar_link, message, date_time, date_time))
        #cls.conn.commit()

        # Take database
        query = "SELECT * FROM chat"
        cursor.execute(query)
        result = cursor.fetchall()
        #print(result)

        # Return to JSON
        data = {
            "group_name": "GROUP MESSAGE",
            "messages": []
        }

        for row in result:
            print(row)
            message = {
                "message_id": str(row[0]),
                "sender_user_id": row[1],
                "receiver_name": row[2],
                "message_text": row[3],
                "date": str(row[4])
            }
            data["messages"].append(message)

        # Write to JSON 
        with open(cls.FILE_PATH, "w") as json_file:
            json.dump(data, json_file, indent=2)

        # Close connection
        cursor.close()
        
    #@classmethod
    #def get_chat(cls):
        #try:
            #with open(cls.FILE_PATH, 'r') as file:
                #data = json.load(file)

            
            #chat_list = []
            #for message in data["messages"]:
                #chat = {
                    #"sender_name": message["sender_name"],
                    #"avatar_link": message["avatar_link"],
                    #"last_message": message["message"],
                    #"datetime": f"{message['date']} {message['time']}"
                #}
                #chat_list.append(chat)

            #return chat_list
        #except FileNotFoundError:
            #print(f"File not found: {cls.FILE_PATH}")
            #return []
#Chat.create_chat()


def get_active_chats_for_user(user_id):
    pass
# check chat_user and find the unique group names that user is engaged
# 
    #return
    [
        {
            "avatar_link": "link",
            "sender_name": "If group, group name",
            "message_id": "id",
            "group_id": "uuid",
            "last_message": "if group , last message in group",
            "unread_count": "2"
        }
    ]
    # sender veya receiver user_idye esit olanlar , vice versa kombinasyonlar
    # 2-3 veya 3-2 UNION ALL
    # UNION ALL 
    # sender veya receiverda olup grup mesaji olan gruplarin idlerini bul 
    # bu grup id y ait olan butun kisilerin mesajlarini getir diyeceksiniz. 

    """
    WITH GroupsWithMember1 AS (
        SELECT DISTINCT group_id
        FROM chat_user
        WHERE member_id = 1
    ),
    FirstNonMember1InEachGroup AS (
        SELECT DISTINCT ON (cu.group_id) cu.*
        FROM chat_user cu
        JOIN GroupsWithMember1 gwm1 ON cu.group_id = gwm1.group_id
        WHERE cu.member_id <> 1
        ORDER BY cu.group_id, cu.member_id
    )
    -- Retrieve the latest message in each group with member_id, group_name, and user name
    SELECT
        fm1.group_id,
        fm1.message_id,
        fm1.sender_id,
        fm1.message,
        fm1.created_datetime,
        fnm1.member_id,
        fnm1.group_name,
        u.name AS user_name,
        u.avatar_path as avatar_path
    FROM (
        SELECT
            c.group_id,
            c.message_id,
            c.sender_id,
            c.message,
            c.created_datetime,
            ROW_NUMBER() OVER (PARTITION BY c.group_id ORDER BY c.created_datetime DESC) AS message_rank
        FROM chat c
        JOIN FirstNonMember1InEachGroup fnm1 ON c.group_id = fnm1.group_id
    ) AS fm1
    JOIN FirstNonMember1InEachGroup fnm1 ON fm1.group_id = fnm1.group_id
    JOIN "user" u ON fnm1.member_id = u.user_id
    WHERE fm1.message_rank = 1;
    """






def get_specific_communication(message_id, group_id):
    pass
    [
        {
            "avatar_link": "link",
            "sender_name": "If group, group name",
            "sender_id": "id",
            "receiver_id": "id",
            "datetime" : "datetime",
            "message_id": "id",
            "group_id": "0 veya uuid",
            "message": "message"
        }
    ]

    """
    select
    c.message_id ,
    c.sender_id,
    c.group_id,
    c.message,
    c.created_datetime,
    u."name" ,
    u.last_name ,
    u.user_type,
    u.status,
    u.avatar_path
    from chat c
    left join "user" u on c.sender_id = u.user_id 
    where group_id = '4b017c84-493c-41a2-8d1d-6e06fc4c5e8b'
    order by created_datetime asc
    """

    """
    select * from chat_user cu 
    where group_id = '4b017c84-493c-41a2-8d1d-6e06fc4c5e8b'
    """

def create_message():
    pass

def send_reply():
    pass

def get_users_for_message(user_id):
    pass
# o user id disindaki kisilerin bilgileri , passive olmayanlarin
# user_id, isim ve user_type


def create_group(user_list, group_name):
    with get_db_connection() as conn:
        try:
            with conn.cursor() as cursor:
                # Generate a new UUID for the group_id
                group_id = str(uuid.uuid4())

                # Insert the new group into the chat_user table
                for user_id in user_list:
                    cursor.execute(
                        "INSERT INTO school.chat_user (group_id, member_id, group_name) VALUES (%s, %s, %s)",
                        (group_id, user_id, group_name)
                    )

                # Commit the changes to the database
                conn.commit()

                print(f"Group '{group_name}' with ID {group_id} created successfully.")
        except Exception as e:
            print(f"Error: {e}")


# Example usage:
user_list = [3, 4]  # Replace with actual user IDs
group_name = "NewGroup"  # Replace with the desired group name
create_group(user_list, group_name)



