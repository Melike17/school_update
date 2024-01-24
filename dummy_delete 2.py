import sys, os
sys.path.append(os.getcwd())
from datetime import datetime

from Classes.user import User

group_name = "test"
member_list = [1, 2, 3]
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%d %b - %H:%M")
User.update_user_last_seen(2,formatted_datetime)