import sys, os
sys.path.append(os.getcwd())
from itertools import zip_longest

from PyQt5.QtWidgets import QSpacerItem, QSizePolicy,QMessageBox,QGroupBox, QAbstractItemView, QApplication, QMainWindow, QVBoxLayout, QLabel, QListWidgetItem, QListWidget, QHBoxLayout, QWidget, QCheckBox
from PyQt5 import QtGui, QtCore
from Ui_chat_mobil import Ui_MainWindow
from Classes.user import User
import datetime, time

selected_usersfor_group_creation = set()


#User.set_currentuser("student@example.com")

class MessagesUpdater(QtCore.QThread):
    messagesUpdated = QtCore.pyqtSignal(list)
    def __init__(self):
        super(MessagesUpdater, self).__init__()
        self.stop_thread = False
        self.current_index = 0

    def run(self):
        while not self.stop_thread:
            if self.current_index == 0:
                #print("Thread-chat")
                new_active_messages = User.get_latest_messages_for_member(User._current_user.user_id)
                self.messagesUpdated.emit(new_active_messages)
                self.msleep(1000)
            self.msleep(200)

    def stop(self):
        print("Message updater is stopping")
        self.stop_thread = True
        self.wait()
    
    def set_current_index(self, current_index):
        self.current_index = current_index

class UnreadChecker(QtCore.QThread):
    is_read_updated = QtCore.pyqtSignal(list)
    def __init__(self):
        super(UnreadChecker, self).__init__()
        self.unread_message_list = None
        self.stop_thread = False
        self.current_index = 0

    def run(self):
        while not self.stop_thread:
            if self.current_index == 1:
                #print("Thread-unread check")
                message_new_status = User.check_read_status_for_unread_messages(self.unread_message_list)
                #print(f"Unread status current, message id {self.unread_message_list}")
                #print(message_new_status)
                if message_new_status is not None:
                    self.is_read_updated.emit(message_new_status)
                self.msleep(1000)
            self.msleep(200)

    def set_current_index(self, current_index):
        self.current_index = current_index

    
    def set_status(self,unread_message_list):
        self.unread_message_list = unread_message_list
    

    def stop(self):
        self.stop_thread = True
        self.wait()

class SpecificMessageUpdater(QtCore.QThread):
    specificMessageUpdated = QtCore.pyqtSignal(list)

    def __init__(self):
        super(SpecificMessageUpdater, self).__init__()
        self.stop_thread = False
        self.current_index = None

    def set_current_index(self, current_index):
        self.current_index = current_index
    
    def set_status(self,user_id, group_id, current_message_count):
        self.user_id = user_id
        self.group_id = group_id
        self.current_message_count = current_message_count

    def run(self):
        
        while not self.stop_thread:
            if self.current_index == 1:
                #print("Thread_ active message check")
                new_message_count = User.get_count_message_for_group(self.group_id)
                #print(f"Current Message count: {self.current_message_count}, new count from db: {new_message_count} ")
                if self.current_message_count == new_message_count:
                    pass
                    #print("Same message count, do not update GUI")
                else:
                    #print("New messages found, sending to GUI")
                    new_messages = User.get_specific_communication(self.group_id,self.user_id)
                    self.specificMessageUpdated.emit([new_message_count,new_messages])
                self.msleep(1000)
            self.msleep(200)

    def stop(self):
        print("Specific message updater is stopping")
        self.stop_thread = True
        self.wait()


class ChatStatusUpdater(QtCore.QThread):
    chat_status_updated = QtCore.pyqtSignal()

    def __init__(self, group_id, user_id, parent=None):
        super(ChatStatusUpdater, self).__init__(parent)
        self.group_id = group_id
        self.user_id = user_id
        self.current_index = 0
        self.stop_thread = False
        self.status = ""
        self.db_status = True

    def run(self):
        while not self.stop_thread:
            if self.current_index == 1 and self.db_status: 
                #current user is typing
                #print(f"Current user is typing thread working with status: {self.status}, group_id {self.group_id}, user {self.user_id}")
                User.update_user_status(self.group_id, self.user_id, self.status)
                #self.db_status = False
                self.chat_status_updated.emit()
                self.msleep(2000)
            self.msleep(500)

    def set_current_index(self, current_index):
        self.current_index = current_index

    def initiate(self):
        self.db_status = True
    
    def set_status(self, status, group_id, user_id):
        self.status = status
        self.group_id = group_id
        self.user_id = user_id

    def stop(self):
        print("User status updating stopping")
        self.stop_thread = True
        self.wait()

#send new message to db - one time run
class NewMessageSentUpdater(QtCore.QThread):
    new_message_sent = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(NewMessageSentUpdater, self).__init__(parent)
        self.user_id = None,
        self.group_id = None,
        self.message = None,
        self.member_list = None

    def run(self):
        #current user is typing
        print("New message sent thread working")
        message_id = User.send_message(self.user_id,self.group_id,self.message,self.member_list)
        self.new_message_sent.emit(message_id)

    def set_status(self, user_id,group_id,message,member_list):
        self.user_id = user_id,
        self.group_id = group_id,
        self.message = message,
        self.member_list = member_list
     
class UserStatusUpdater(QtCore.QThread):
    UserStatusUpdated = QtCore.pyqtSignal(list)
    def __init__(self):
        super(UserStatusUpdater, self).__init__(parent=None)
        self.group_id = None
        self.user_id = None
        self.current_status = None
        self.initial_status = None
        self.typing_count = None
        self.user_count = None
        self.stop_thread = False
        self.current_index = None

    def set_status(self, group_id, user_id, current_status,initial_status,typing_count,user_count):
        self.group_id = group_id
        self.user_id = user_id
        self.current_status = current_status
        self.initial_status = initial_status
        self.typing_count = typing_count
        self.user_count = user_count

    def set_current_index(self, current_index):
        self.current_index = current_index
        #print(f"thread user status index has been updated to {self.current_index}, new index = {current_index}")

    def run(self):
        while not self.stop_thread:
            if self.current_index == 1: 
                #print("Thread -- User status updater")
                db_typing_count = User.get_typing_count(self.group_id,self.user_id)
                print(f"Db typing count {db_typing_count} ")
                db_user_info = User.get_message_user_info(self.group_id, self.user_id)
                status_value = db_user_info[0][7]
                if (self.typing_count == db_typing_count) and (db_user_info[0][7] == self.initial_status):
                    #print("User status updater thread - No chnage found")
                    pass
                else:
                    is_group = self.user_count > 2
                    db_typing_list = User.get_other_user_typing_status(self.group_id,self.user_id)
                    #print (f"typing list {db_typing_list}")
                    if len(db_typing_list) == 0:
                        #print("User status updater thread - Nobody is typing")
                        if is_group:
                            formatted_text = self.initial_status
                        else:
                            if status_value == "Online":
                                formatted_text = "Online"
                            elif status_value is None:
                                formatted_text = "No status"
                            else:
                                formatted_text = "Last seen: " + status_value
                    elif len(db_typing_list) == 1:
                        formatted_text =  f"{db_typing_list[0][0]} is typing."
                    elif len(db_typing_list) == 2:
                        formatted_text = f"{db_typing_list[0][0]} and {db_typing_list[1][0]} are typing."
                    else:
                        additional_users = len(db_typing_list) - 2
                        formatted_text = f"{db_typing_list[0][0]}, {db_typing_list[1]}, and {additional_users} others are typing." 
                    #print(f"User status updater thread -{formatted_text}, other_user_status = {status_value}")
                    self.UserStatusUpdated.emit([db_typing_count,formatted_text,status_value])
                self.msleep(1000)
            self.msleep(200)

    def stop(self):
        print("User status updating stopping")
        self.stop_thread = True
        self.wait()

class MemberListWidget(QWidget):
    def __init__(self):
        super(MemberListWidget, self).__init__()

        self.member_label = self.findChild(QLabel, 'specific_status_label')

        self.member_list = QListWidget()
        self.member_list.addItem(QListWidgetItem("Member 1"))
        self.member_list.addItem(QListWidgetItem("Member 2"))
        self.member_list.addItem(QListWidgetItem("Member 3"))

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.member_label)
        self.layout.addWidget(self.member_list)
        self.member_list.hide()

    def enterEvent(self, event):
        self.member_list.show()

    def leaveEvent(self, event):
        self.member_list.hide()

class SelectedMessageItemWidget(QWidget):
    def __init__(self, avatar_path, username, message, datetime,group_read, is_active_user=False):
        super(SelectedMessageItemWidget, self).__init__()

        self.avatar_label = QLabel(self)
        avatar_pixmap = QtGui.QPixmap(avatar_path).scaledToWidth(30).scaledToHeight(30, QtCore.Qt.SmoothTransformation)

        # Create a circular mask
        mask = QtGui.QBitmap(avatar_pixmap.size())
        mask.fill(QtCore.Qt.color0)
        painter = QtGui.QPainter(mask)
        painter.setBrush(QtCore.Qt.color1)
        painter.drawEllipse(0, 0, mask.width(), mask.height())
        painter.end()

        # Apply the circular mask to the avatar
        avatar_pixmap.setMask(mask)

        self.avatar_label.setPixmap(avatar_pixmap)
        self.avatar_label.setFixedSize(30, 30)
        self.avatar_label.setScaledContents(True)

        # Icon Label
        self.icon_label = QLabel(self)
        icon_path = "files/read_tick.png" if group_read else "files/sent_tick.png"
        icon_pixmap = QtGui.QPixmap(icon_path)
        scaled_pixmap = icon_pixmap.scaled(15, 15, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        self.icon_label.setPixmap(scaled_pixmap)
        self.icon_label.setMaximumSize(15, 15)
        self.icon_label.setVisible(is_active_user)

        # Message Group
        message_group_layout = QVBoxLayout()

        # Message Label
        self.message_label = QLabel(message, self)

        # Calculate label width
        label_width = self.message_label.fontMetrics().boundingRect(self.message_label.text()).width()

        # Set maximum width (adjust the value as needed)
        max_width = 300
        self.message_label.setMaximumWidth(max_width)

        # Set fixed width with some extra space
        label_width = QtGui.QFontMetrics(self.message_label.font()).width(message)
        #self.message_label.setFixedWidth(min(label_width + 35, max_width))

        # Apply line break if text is longer than a fixed quantity
        max_chars_before_line_break = 35
        words = message.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) <= max_chars_before_line_break:
                current_line += word + " "
            else:
                lines.append(current_line.rstrip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.rstrip())

        formatted_text = "\n".join(lines)
        self.message_label.setText(formatted_text)

        self.message_label.setStyleSheet(f"font-size: 16px; padding: 6px; border-radius: 10px; background-color: {'#AAD7D9' if is_active_user else '#E5E1DA'}; text-align: center;")
        self.message_label.setAlignment(QtCore.Qt.AlignRight if is_active_user else QtCore.Qt.AlignLeft)

        # Date Time Label
        self.datetime_label = QLabel(datetime, self)
        self.datetime_label.setStyleSheet("font-style: italic; font-size: 13px; color: black; background-color: none;")

        self.datetime_label.setAlignment(QtCore.Qt.AlignLeft if not is_active_user else QtCore.Qt.AlignRight)

        # Add widgets to message group layout
        message_group_layout.addWidget(self.message_label, alignment=QtCore.Qt.AlignRight if is_active_user else QtCore.Qt.AlignLeft)
        message_group_layout.addWidget(self.datetime_label)

        # Main Layout
        main_layout = QHBoxLayout(self)

        if is_active_user:
            main_layout.addLayout(message_group_layout)
            main_layout.addWidget(self.avatar_label, alignment=QtCore.Qt.AlignTop)
            main_layout.addWidget(self.icon_label,alignment=QtCore.Qt.AlignTop)
        else:
            main_layout.addWidget(self.avatar_label, alignment=QtCore.Qt.AlignTop)
            main_layout.addLayout(message_group_layout)

        main_layout.setContentsMargins(5, 5, 5, 5)

class UserListItem(QWidget):
    def __init__(self, user_id, username, surname, user_type, avatar_path):
        super().__init__()

        self.user_id = user_id

        self.checkbox = QCheckBox(self)
        self.checkbox.clicked.connect(self.checkbox_clicked)
        self.checkbox.setStyleSheet("QCheckBox { background: white; } QCheckBox::indicator { width: 30px; height: 30px; }")

        self.setFixedSize(380, 120)
        self.avatar_label = QLabel(self)
        self.avatar_label.setPixmap(QtGui.QPixmap(avatar_path).scaledToWidth(40).scaledToHeight(40, QtCore.Qt.SmoothTransformation))
        self.avatar_label.setFixedSize(40, 40)
        self.avatar_label.setScaledContents(True)
        self.avatar_label.setStyleSheet("border-radius: 25px;")  # Apply rounded clipping mask

        self.username_label = QLabel(f"{username} {surname}", self)
        self.user_type_label = QLabel(user_type, self)
        self.user_type_label.setStyleSheet("font-style: italic;")

        # Create a group box to apply rounding and background
        group_box = QGroupBox(self)
        #group_box.setStyleSheet("QGroupBox {background-color: white; border-radius: 10px;}")
        group_box_layout = QHBoxLayout(group_box)
        group_box_layout.addWidget(self.username_label)
        group_box_layout.addWidget(self.user_type_label)

        # Main layout
        layout = QHBoxLayout(self)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.avatar_label)
        layout.addWidget(group_box)
        layout.setAlignment(QtCore.Qt.AlignLeft)

        group_box = QGroupBox(self)
        group_box.setLayout(layout)
        group_box.setStyleSheet("QGroupBox {background-color: white; border-radius: 10px;}")

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)

    def checkbox_clicked(self):
        #print(f"Checkbox clicked for user: {self.user_id}")
        if self.checkbox.isChecked():
            selected_usersfor_group_creation.add(self.user_id)
        else:
            selected_usersfor_group_creation.discard(self.user_id)
        #print(f"Selected Users: {selected_usersfor_group_creation}")

class MessageItemWidget(QWidget):
    def __init__(self, avatar_path, username, message_preview, unread_count):
        super(MessageItemWidget, self).__init__()

        # Avatar
        self.avatar_label = QLabel(self)
        self.avatar_label.setPixmap(QtGui.QPixmap(avatar_path).scaledToWidth(50).scaledToHeight(50, QtCore.Qt.SmoothTransformation))
        self.avatar_label.setFixedSize(50, 50)
        self.avatar_label.setScaledContents(True)
        self.avatar_label.setStyleSheet("border-radius: 25px;")  # Apply rounded clipping mask

        # User Info
        user_info_layout = QVBoxLayout()
        user_info_layout.setAlignment(QtCore.Qt.AlignTop)  # Align to the top
        user_info_layout.setSpacing(5)  # Set spacing between items

        # Username Group
        username_group_layout = QHBoxLayout()
        self.username_label = QLabel(username, self)
        self.username_label.setStyleSheet("font-weight: bold; color: black;")  # Make username bold
        username_group_layout.addWidget(self.username_label)
        user_info_layout.addLayout(username_group_layout)

        # User Info Group
        user_info_group_layout = QHBoxLayout()
        self.message_preview_label = QLabel(message_preview, self)
        self.message_preview_label.setStyleSheet("padding: 5px; font-style: italic; font-weight: normal; color: black; background-color: white;")

        if unread_count > 0:
            # Make the text bold if unread count is greater than 0
            self.message_preview_label.setStyleSheet(
                "padding: 5px;  font-weight: bold; color: black; background-color: white;"
            )

        self.unread_count_label = QLabel(str(unread_count), self)

        # Set styles for unread count label
        self.unread_count_label.setStyleSheet("background-color: lightcoral; border-radius: 10px; padding: 2px 2px; font-weight: bold;")
        # Add a spacer to the right of unread_count_label
        
        self.unread_count_label.setVisible(unread_count > 0)
        user_info_group_layout.addWidget(self.message_preview_label)
        
        user_info_group_layout.addStretch()  # Add stretch to push unread_count_label to the right
        user_info_group_layout.addWidget(self.unread_count_label)

        user_info_layout.addLayout(user_info_group_layout)
        

        # Main Container Widget
        container_widget = QWidget(self)
        container_layout = QHBoxLayout(container_widget)
        container_layout.addWidget(self.avatar_label)
        container_layout.addLayout(user_info_layout)
        container_layout.setContentsMargins(10, 10, 10, 10)  # Padding
        container_widget.setStyleSheet("background-color: white; border-radius: 10px;")

        # Set background color of the Container Widget
        container_widget.setStyleSheet("background-color: white;")

        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(container_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

class UserItemWidget(QWidget):
    def __init__(self, user_data):
        super(UserItemWidget, self).__init__()

        self.avatar_path = user_data.get("avatar_path", "")

        # Create widgets
        self.avatar_label = QLabel()
        self.avatar_label.setPixmap(QtGui.QPixmap(self.avatar_path).scaledToWidth(50).scaledToHeight(50, QtCore.Qt.SmoothTransformation))
        self.username_label = QLabel(user_data.get("username", ""))
        self.user_type_label = QLabel(user_data.get("user_type", ""))
        self.checkbox = QCheckBox()

        # Layout setup
        layout = QHBoxLayout(self)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.avatar_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.user_type_label)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        User.update_user_last_seen(User._current_user.user_id,"Online")
        self.user_list_to_message = User.get_users_for_search_to_message(User._current_user.user_id)
        self.active_message_widget_type = "message"
        self.message_text_field.is_user_typing = False
        self.selectedMessageList.group_id = None
        self.specific_status_label.initial_status = None
        self.specific_status_label.typing_count = None

        #Thread generation
        self.message_updater = MessagesUpdater()
        self.message_updater.messagesUpdated.connect(self.load_active_messages)
        self.message_updater.start()

        self.specific_message_updater = SpecificMessageUpdater()
        self.specific_message_updater.specificMessageUpdated.connect(self.handleSpecificMessageUpdate)
        self.specific_message_updater.set_status(User._current_user.user_id, None, 0)
        self.specific_message_updater.start()

        self.is_read_updater = UnreadChecker()
        self.is_read_updater.is_read_updated.connect(self.handleReadingStatus)
        unread_list = getattr(self.selectedMessageList, 'unread_message_list', [])
        self.is_read_updater.set_status(unread_list)
        self.is_read_updater.start()

        self.new_message_sender = NewMessageSentUpdater()
        self.new_message_sender.new_message_sent.connect(self.new_message_sent)

        #def __init__(self, group_id, user_id, current_status,initial_status,typing_count,user_count, parent=None):
        self.user_status_updater = UserStatusUpdater()
        self.user_status_updater.UserStatusUpdated.connect(self.handleUserStatusUpdate)
        self.user_status_updater.start()

        self.chat_status_updater = ChatStatusUpdater(self.selectedMessageList.group_id, User._current_user.user_id)
        self.chat_status_updater.chat_status_updated.connect(self.handleChatStatus)
        self.chat_status_updater.start()
        
 

        self.stackedWidget.setCurrentIndex(0)
        self.selectedMessageList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.messageListWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.select_group_members_list.setSelectionMode(QAbstractItemView.NoSelection)
        self.select_group_members_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        self.set_profile_avatar()
        
        
        self.messageListWidget.itemClicked.connect(self.active_message_or_user_clicked)
        self.back_button_2.clicked.connect(lambda: self.go_to_page(page_no="0"))
        self.back_button2.clicked.connect(lambda: self.go_to_page(page_no="0"))
        self.redirect_create_group_button.clicked.connect(lambda: self.go_to_page(page_no="2"))
        self.create_group_button.clicked.connect (self.create_group_flow)
        self.send_message_button.clicked.connect(self.send_message)

        self.user_search_for_group_label.textChanged.connect(self.filter_Users_in_Group_Create)
        self.user_search_for_group_label.textChanged.connect(self.filter_Users_in_Group_Create)
        self.user_search.textChanged.connect(self.updateListWidget)

        #self.message_text_field.textChanged.connect(self.change_user_status)
    
        self.go_to_page(page_no="0")

    def set_thread_page_status(self,index):
        self.user_status_updater.set_current_index(index)
        self.message_updater.set_current_index(index)
        self.specific_message_updater.set_current_index(index)
        self.is_read_updater.set_current_index(index)
        self.chat_status_updater.set_current_index(index)


    def go_to_page(self,page_no):
        # 0 active chat groups // 1 message // 2 create group,
        self.user_search.clear()

        if int(page_no) == 0 :
            self.set_thread_page_status(0)
            self.stackedWidget.setCurrentIndex(int(page_no))
        elif int(page_no) == 2:
            self.load_group_users_for_creation()
            self.set_thread_page_status(2)
            self.stackedWidget.setCurrentIndex(int(page_no))
            
        else:
            self.set_thread_page_status(1)
            self.specific_message_updater.current_index = 1
            self.load_message_user_info(self.selectedMessageList.group_id,User._current_user.user_id)
            message_count = self.selectedMessageList.count() or 0
            print(f"current message count is {message_count}")
            self.specific_message_updater.set_status(User._current_user.user_id,
                                                     self.selectedMessageList.group_id,
                                                     message_count
                                                     )
            self.user_status_updater.set_status(self.selectedMessageList.group_id,
                                                User._current_user.user_id,
                                                self.specific_status_label.text(),
                                                self.specific_status_label.initial_status,
                                                self.specific_status_label.typing_count,
                                                len(self.selectedMessageList.member_list)
                                                )
            if not self.user_status_updater.isRunning():
                self.user_status_updater.start()
            
            unread_list = getattr(self.selectedMessageList, 'unread_message_list', [])
            self.is_read_updater.set_status(unread_list)
            print("Thread initiated from pagecontrol. group-id for message loading", self.selectedMessageList.group_id, "Message_count", message_count )
            QtCore.QTimer.singleShot(500,lambda: self.stackedWidget.setCurrentIndex(int(page_no)))
            self.chat_status_updater.set_status("",self.selectedMessageList.group_id, User._current_user.user_id)
        

    def handleUserStatusUpdate(self,result_list):
        #[db_typing_count,formatted_text]
        db_typing_count, formatted_text, new_initial_status = result_list
        self.specific_status_label.initial_status = new_initial_status if self.specific_status_label.initial_status != new_initial_status else self.specific_status_label.initial_status
        self.specific_status_label.typing_count = db_typing_count # after emit it will be set, first 0 
        self.specific_status_label.setText(formatted_text)  # after emit will be set
        self.user_status_updater.set_status(self.selectedMessageList.group_id,
                                                User._current_user.user_id,
                                                self.specific_status_label.text(),
                                                self.specific_status_label.initial_status,
                                                self.specific_status_label.typing_count,
                                                len(self.selectedMessageList.member_list)
                                                )

    def handleReadingStatus(self,update_list):
        print("Reading status function triggered")
        print(f"update list is {update_list}")
        first_elements_list = [update_tuple[0] for update_tuple in update_list]

        for index in range(self.selectedMessageList.count() - 1, -1, -1):
            listWidgetItem = self.selectedMessageList.item(index)
            stored_message_id = listWidgetItem.data(QtCore.Qt.UserRole)
            print(f"message needs tick update {stored_message_id}")
            if stored_message_id in first_elements_list:
                self.update_read_tick_for_message(index)
                print("Reading status function found message that is read - Updating ui tick icon")
                #message_widget = self.selectedMessageList.itemWidget(listWidgetItem)
                #message_widget.set_read_status(True)
                self.selectedMessageList.unread_message_list.remove(stored_message_id)
                

        self.selectedMessageList.unread_message_list
        unread_list = getattr(self.selectedMessageList, 'unread_message_list', [])
        self.is_read_updater.set_status(unread_list)

    def update_read_tick_for_message(self,index_to_change):
        group_read = True
        is_active_user = True
        # Access the item at the specified index
        item_to_change = self.selectedMessageList.item(index_to_change)

        # Check if the item exists before attempting to update it
        if item_to_change:
            # Access the custom widget associated with the item
            message_item_widget = self.selectedMessageList.itemWidget(item_to_change)

            # Check if the custom widget exists and has the icon_label attribute
            if message_item_widget and hasattr(message_item_widget, 'icon_label'):
                # Update the icon_label based on your logic
                icon_path = "files/read_tick.png" if group_read else "files/sent_tick.png"
                icon_pixmap = QtGui.QPixmap(icon_path)
                scaled_pixmap = icon_pixmap.scaled(15, 15, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

                message_item_widget.icon_label.setPixmap(scaled_pixmap)
                message_item_widget.icon_label.setMaximumSize(15, 15)
                message_item_widget.icon_label.setVisible(is_active_user)
        else:
            print(f"Item at index {index_to_change} not found")

    def new_message_sent(self,message_id):
        print(f"New message sent thread finished, function triggered - message id: {message_id}")
        self.selectedMessageList.unread_message_list.append(message_id)
        for index in range(self.messageListWidget.count() - 1, -1, -1):
            listWidgetItem = self.messageListWidget.item(index)
            stored_message_id = listWidgetItem.data(QtCore.Qt.UserRole)
            if stored_message_id == "new_message":
                listWidgetItem.setData(QtCore.Qt.UserRole+2, message_id)
        print(f"New message sent thread finished, function triggered - message id:{message_id} unread list {self.selectedMessageList.unread_message_list}" )
        

    def load_message_user_info(self,group_id,user_id):
        print("Load user info function is running")
        result_group_info = User.get_message_user_info(group_id,user_id)
        if len(result_group_info) >1:
            print("Message is a group message")
            display_name = result_group_info[0][2]
            avatar_path = "avatars/group.png"
            status = str(len(result_group_info)+1) + ' ' +  "Members"
            self.specific_status_label.setToolTip("\n".join(self.generate_tooltip_html(result_group_info)))
        else:
            #print(result_group_info)
            print("Message is between 2 person")
            self.specific_status_label.setToolTip(None)
            display_name = result_group_info[0][3] + ' ' + result_group_info[0][4]
            avatar_path = result_group_info[0][6]

            status_value = result_group_info[0][7]
            if status_value == "Online":
                status = "Online"
            elif status_value is None:
                status = "No status"
            else:
                status = "Last seen: " + status_value
        self.selectedMessageList.member_list = set([item[1] for item in result_group_info])
        self.selectedMessageList.member_list.add(User._current_user.user_id)
        print(f"member list is set as : {self.selectedMessageList.member_list}")
        # Create a circular mask
        avatar_pixmap = QtGui.QPixmap(avatar_path)
        mask = QtGui.QBitmap(avatar_pixmap.size())
        mask.fill(QtCore.Qt.color0)
        painter = QtGui.QPainter(mask)
        painter.setBrush(QtCore.Qt.color1)
        painter.drawEllipse(0, 0, mask.width(), mask.height())
        painter.end()

            # Apply the circular mask to the avatar
        avatar_pixmap.setMask(mask)

        self.specific_avatar_label.setPixmap(avatar_pixmap)
        self.specific_avatar_label.setFixedSize(50, 50)
        self.specific_avatar_label.setScaledContents(True)

        self.specific_status_label.setText(status)
        self.specific_status_label.initial_status = status
        self.specific_status_label.typing_count = 0
        self.specific_username_label.setText(str(display_name))

    def updateListWidget(self):
        self.messageListWidget.clear()
        if len(self.user_search.text()) == 0:
            self.active_message_widget_type = "message"
            self.load_active_messages(self.messageListWidget.messages)
            #DEV userdan mesaja donerken bosuna tekrar cagirma, listwidget ustundekinden getir
        else:
            self.active_message_widget_type = "user"
            search_text = self.user_search.text().lower()
            filtered_user_list = [user for user in self.user_list_to_message if search_text in user[1].lower() or search_text in user[2].lower() or search_text in user[3].lower() ]
            self.load_user_search(filtered_user_list)
        
    
        
    #is not used depriciated
    def handleMessagesUpdate(self, new_messages):
        if self.stackedWidget.currentIndex() == 0 and self.active_message_widget_type == "message":
            are_equal = len(set(new_messages + self.messageListWidget.messages)) == len(self.messageListWidget.messages)
            if not are_equal:
                pass
                #print(f"message count is not equal, loading again, are_eqaul = {are_equal}")
                

    def handleSpecificMessageUpdate(self,response):
        self.selectedMessageList.clear()
        new_message_count,new_messages = response
        result_messages = sorted(new_messages, key=lambda x: x[4])
        for message_data in result_messages :
            message_id,sender_id,group_id,message,created_datetime,name,last_name,user_type,avatar_path, is_read, group_read = message_data
            
            formatted_date = created_datetime.strftime("%I:%M %p")
            is_current_user = True if sender_id == User._current_user.user_id else False
            self.addselectedmessage(avatar_path, name, message, formatted_date,group_read, is_current_user,message_id)


        print("Inserting new message in chat. Message count", new_message_count)
        self.selectedMessageList.message_count = new_message_count
        self.selectedMessageList.unread_message_list = [item[0] for item in result_messages if item[10] != True ]
        print(f"Message first load, unread message list {self.selectedMessageList.unread_message_list}")
        self.selectedMessageList.unread_by_user = [item[0] for item in result_messages if item[9] != True ]
        last_item = self.selectedMessageList.item(self.selectedMessageList.count() - 1)
        self.selectedMessageList.scrollToItem(last_item)

        result = User.insert_message_read(User._current_user.user_id, self.selectedMessageList.unread_by_user)
        print(f"Unread insert is completed:  {result}")

        self.specific_message_updater.set_status(User._current_user.user_id,
                                                     self.selectedMessageList.group_id,
                                                     new_message_count
                                                     )
        unread_list = getattr(self.selectedMessageList, 'unread_message_list', [])
        self.is_read_updater.set_status(unread_list)


    def handleChatStatus(self):
        #print(f" Parameters {self.message_text_field.toPlainText()} length: {len(self.message_text_field.toPlainText())} and  {self.message_text_field.is_user_typing}")
        if len(self.message_text_field.toPlainText()) == 0:
            # and self.message_text_field.is_user_typing == True
            ## generate only once when needed
            #def __init__(self, group_id, user_id, status, parent=None):
            self.chat_status_updater.set_status("",self.selectedMessageList.group_id, User._current_user.user_id)
            #self.message_text_field.is_user_typing == False
            self.chat_status_updater.initiate()
            #print("user stopped typing")
        elif len(self.message_text_field.toPlainText()) > 0:
            # and self.message_text_field.is_user_typing == False
            self.chat_status_updater.set_status("typing",self.selectedMessageList.group_id, User._current_user.user_id)
            #self.message_text_field.is_user_typing == True
            self.chat_status_updater.initiate()
            print("user started typing")
        else:
            pass

    def closeEvent(self, event):
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%d %b - %H:%M")
        User.update_user_last_seen(User._current_user.user_id,formatted_datetime)
        if self.is_typing_timer.isActive():
            self.is_typing_timer.stop()
        if self.user_status_updater.isRunning():
            self.user_status_updater.stop()
        if self.specific_message_updater.isRunning():
            self.specific_message_updater.stop()
        if self.message_updater.isRunning():
            self.message_updater.stop()
        if self.is_read_updater.isRunning():
            self.is_read_updater.stop()
        if self.chat_status_updater.isRunning():
            self.chat_status_updater.stop()
        #self.repeating_timer.stop()

    def set_profile_avatar(self):
        start_time = time.time()
        #self.current_user_avatar_label = QLabel(self)
        self.current_user_avatar_label.setPixmap(QtGui.QPixmap(User._current_user.avatar_path).scaledToWidth(50).scaledToHeight(50, QtCore.Qt.SmoothTransformation))
        self.current_user_avatar_label.setFixedSize(50, 50)
        self.current_user_avatar_label.setScaledContents(True)
        self.current_user_avatar_label.setStyleSheet("border-radius: 25px;")  # Apply rounded clipping mask
        self.profile_name_label.setText(User._current_user.name + " " + User._current_user.surname)
        # User Info
        user_info_layout = QVBoxLayout()
        user_info_layout.setAlignment(QtCore.Qt.AlignTop)  # Align to the top
        user_info_layout.setSpacing(5)  # Set spacing between items
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time for profile avatar: {elapsed_time} seconds")

    def send_message(self):
        start_time = time.time()
        message = self.message_text_field.toPlainText()
        if message == "":
            pass
        elif self.selectedMessageList.group_id:
            self.message_text_field.clear()

            self.new_message_sender.set_status(User._current_user.user_id,self.selectedMessageList.group_id,message,self.selectedMessageList.member_list)
            self.new_message_sender.start()
            
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            #def addselectedmessage(self, avatar_path, username, message_preview, time,group_read, is_active_user,message_id):
            self.addselectedmessage(User._current_user.avatar_path,
                                    User._current_user.name,
                                    message,
                                    current_time,
                                    False,
                                    is_active_user=True,
                                    message_id="new_message")
            # update message quanttiy so it doesnt load messages again., job will handle , read status ve new messege from others.
            self.selectedMessageList.message_count += 1
            # scroll to last message
            last_item = self.selectedMessageList.item(self.selectedMessageList.count() - 1)
            self.selectedMessageList.scrollToItem(last_item)
            User.update_chat_status(User._current_user.user_id, self.selectedMessageList.group_id,self.selectedMessageList.member_list)
        else:
            self.showUpdateAlert("Problem exists in send message function")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time for send message: {elapsed_time} seconds")
        

    def filter_Users_in_Group_Create(self):
        search_text = self.user_search_for_group_label.text().lower()

        for index in range(self.select_group_members_list.count()):
            item = self.select_group_members_list.item(index)
            user_widget = self.select_group_members_list.itemWidget(item)
            username = user_widget.username_label.text().lower()
            user_type = user_widget.user_type_label.text().lower()

            if search_text in username or search_text in user_type:
                item.setHidden(False)
            else:
                item.setHidden(True)

    def load_group_users_for_creation(self):
        users_data = User.get_users_for_group_create(User._current_user.user_id)
        for user_data in users_data:
            user_id, username, surname, _, _, _, _, _, user_type, _, avatar_path, _ = user_data

            user_item = QListWidgetItem(self.select_group_members_list)
            user_widget = UserListItem(user_id, username, surname, user_type, avatar_path)
            user_item.setSizeHint(user_widget.sizeHint())
            self.select_group_members_list.addItem(user_item)
            self.select_group_members_list.setItemWidget(user_item, user_widget)
            


    def showUpdateAlert(self, alert):
        message = alert
        QMessageBox.information(None, "Item Updated", message, QMessageBox.Ok)

    def create_group_flow(self):
        if self.group_name_label.text() == "":
            self.showUpdateAlert("Group Name cannot be empty!")
        elif len(selected_usersfor_group_creation) == 0:
            self.showUpdateAlert("Please select users to create group")
        else:
            group_name = self.group_name_label.text()
            selected_usersfor_group_creation.add(User._current_user.user_id)
            group_id = User.create_message_group(group_name=group_name,member_list=selected_usersfor_group_creation)
            selected_usersfor_group_creation.clear()
            self.load_group_users_for_creation()
            self.showUpdateAlert("Group is created. Click ok to redirect to group message")
            #self.load_specific_message(group_id)
            self.selectedMessageList.group_id = group_id
            self.go_to_page(1)


    def active_message_or_user_clicked(self,item):
        print(f"Widget type is {self.active_message_widget_type}")
        if self.active_message_widget_type == "user":
            group_id = item.data(QtCore.Qt.UserRole)
            other_user_id = item.data(QtCore.Qt.UserRole+1)
            print(f"User card is clicked, group id: {group_id}, user_id: {other_user_id}")
            if group_id == "": #ekstra kontrol
                group_id_array = User.check_group_id_of_users(User._current_user.user_id,other_user_id)
                if len(group_id_array) == 1:
                    #self.load_specific_message(group_id_array[0])
                    self.selectedMessageList.group_id = group_id_array[0]
                    self.go_to_page(1)
                elif len(group_id) == 0:
                    created_group_id = User.create_message_group("",[User._current_user.user_id,other_user_id])
                    #self.load_specific_message(created_group_id)
                    self.selectedMessageList.group_id = created_group_id
                    self.go_to_page(1)
        else:
            group_id = item.data(QtCore.Qt.UserRole)
            #print(f"message group id is clicked id={group_id}")
            #self.load_specific_message(group_id)
            self.selectedMessageList.group_id =group_id
            self.go_to_page(1)

    def generate_tooltip_html(self,data):
        # Assuming data is a tuple with the format (index3, username, last_name, user_type)
        tooltips = [
    f"<html><body style='width: 200px; border-bottom: 1px solid gray;'><p style='margin:0;'><b>{username} {last_name}</b></p><p style='margin:0;'><i>{user_type}</i></p>"
    f"<p style='margin:0;'><img src='{avatar_path}' alt='Avatar' width='30' height='30'></p>" if avatar_path else ""
    f"<p style='margin:0; font-size: smaller;'><i>{status}</i></p>" if status else ""
    "</body></html>"
    for _, _, username, user_type, last_name, _, avatar_path, status in data
]

        return tooltips

    # is not used anymore
    def load_specific_message(self,group_id):
        self.selectedMessageList.clear()
        self.selectedMessageList.group_id = group_id
        #print("Property of list widget", self.selectedMessageList.group_id)


        result_messages = User.get_specific_communication(group_id,User._current_user.user_id)
        result_messages = sorted(result_messages, key=lambda x: x[4])
        #print(result_group_info)
        for message_data in result_messages :
            message_id,sender_id,group_id,message,created_datetime,name,last_name,user_type,avatar_path, is_read, group_read = message_data
            
            formatted_date = created_datetime.strftime("%I:%M %p")
            is_current_user = True if sender_id == User._current_user.user_id else False
            self.addselectedmessage(avatar_path, name, message, formatted_date,group_read, is_current_user,message_id)

        self.selectedMessageList.message_count = len(result_messages)
        print(f"result message length is {len(result_messages)}, and set as : {self.selectedMessageList.message_count} ")

        self.selectedMessageList.unread_message_list = [item[0] for item in result_messages if item[9] != True ]
        #print(result_messages)
        print(f"Unread message id list is: {self.selectedMessageList.unread_message_list}")
        
        result = User.insert_message_read(User._current_user.user_id, self.selectedMessageList.unread_message_list)
        print(f"Unread insert is completed:  {result}")

        last_item = self.selectedMessageList.item(self.selectedMessageList.count() - 1)
        self.selectedMessageList.scrollToItem(last_item)

    def load_active_messages(self, new_messages):
        if self.active_message_widget_type != "user":
            self.messageListWidget.clear()
        active_messages = new_messages
        active_messages.sort(key=lambda x: x[4] or datetime.datetime.min, reverse=True)
        print("Active messages is updating")
        for message_data in active_messages:
            group_id, message_id, sender_id, message_text, created_datetime, member_id, group_name, sender_name, avatar_path, unread_count = message_data
            display_name = group_name if group_name != "" else sender_name
            avatar_path =  avatar_path if group_name == "" else "avatars/group.png"
            formatted_message = "Group Created" if message_text is None else message_text
            message_length = 30
            if User._current_user.user_id == sender_id:
                if len(formatted_message)+5 >= message_length:
                    formatted_message = "You: " + formatted_message[:message_length-5] + "..."
                else:
                    formatted_message = "You: " + formatted_message
            else:
                if len(formatted_message+sender_name) >= message_length:
                    formatted_message = sender_name + ": " + formatted_message[:message_length-len(sender_name)] + "..."
                else:
                    formatted_message = sender_name + ": " + formatted_message
            #display_name = "test"
            if not (group_name == "" and message_id is None) or (group_name !=""):
                if self.active_message_widget_type != "user":
                    self.addMessage(avatar_path, display_name, formatted_message, unread_count ,group_id)
        self.messageListWidget.messages = active_messages

    def addMessage(self, avatar_path, username, message_preview, unread_count, group_id, user_id = None):
        message_item = MessageItemWidget(avatar_path, username, message_preview, int(unread_count))

        listWidgetItem = QListWidgetItem(self.messageListWidget)  # Use messageListWidget
        listWidgetItem.setSizeHint(message_item.sizeHint())
        listWidgetItem.setData(QtCore.Qt.UserRole, group_id)
        if user_id != None:
            listWidgetItem.setData(QtCore.Qt.UserRole +1, user_id)
        # Make the item non-selectable
        listWidgetItem.setFlags(listWidgetItem.flags() & ~QtCore.Qt.ItemIsSelectable)

        self.messageListWidget.addItem(listWidgetItem)
        self.messageListWidget.setItemWidget(listWidgetItem, message_item)

    def load_user_search(self,user_list):
        self.messageListWidget.clear()
        #print(User._current_user.user_id)
        for user in user_list:
            user_id, name, last_name, user_type, avatar_path = user
            avatar_path =  avatar_path if user_type != "" else "avatars/group.png"
            self.addMessage(avatar_path, name + ' ' + last_name, "", 0, "", user_id=user_id)
        

    def addselectedmessage(self, avatar_path, username, message_preview, time,group_read, is_active_user,message_id):
        selected_message_item = SelectedMessageItemWidget(avatar_path, username, message_preview, time, group_read, is_active_user)
        selectedListWidgetItem = QListWidgetItem(self.selectedMessageList)  # Use selectedMessageList
        selectedListWidgetItem.setSizeHint(selected_message_item.sizeHint())
        selectedListWidgetItem.setData(QtCore.Qt.UserRole, message_id)   
             

        self.selectedMessageList.addItem(selectedListWidgetItem)
        self.selectedMessageList.setItemWidget(selectedListWidgetItem, selected_message_item)

    
    def addUser(self, user_data):
        user_item = UserItemWidget(user_data)
        listWidgetItem = QListWidgetItem(self.user_list)
        listWidgetItem.setSizeHint(user_item.sizeHint())
        self.user_list.addItem(listWidgetItem)
        self.user_list.setItemWidget(listWidgetItem, user_item)

    def filterUsers(self):
        search_text = self.user_search.text().lower()

        for index in range(self.user_list.count()):
            item = self.user_list.item(index)
            widget = self.user_list.itemWidget(item)
            username = widget.username_label.text().lower()
            user_type = widget.user_type_label.text().lower()

            # Check if search text matches username or user type
            if search_text in username or search_text in user_type:
                item.setHidden(False)
            else:
                item.setHidden(True)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
