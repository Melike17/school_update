import csv
import os
import ast
from datetime import datetime
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import json
import psycopg2

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
Chat.create_chat()




