from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QListWidgetItem, QListWidget, QHBoxLayout, QWidget, QCheckBox
from PyQt5 import QtGui, QtCore
from Ui_chat_main import Ui_MainWindow

class SelectedMessageItemWidget(QWidget):
    def __init__(self, avatar_path, username, message, datetime, is_active_user=False):
        super(SelectedMessageItemWidget, self).__init__()

        # Avatar
        self.avatar_label = QLabel(self)
        self.avatar_label.setPixmap(QtGui.QPixmap(avatar_path).scaledToWidth(30).scaledToHeight(30, QtCore.Qt.SmoothTransformation))
        self.avatar_label.setFixedSize(30, 30)
        self.avatar_label.setScaledContents(True)
        self.avatar_label.setStyleSheet("border-radius: 10px; overflow: hidden;")  # Apply rounded clipping mask

        # Message Group
        message_group_layout = QVBoxLayout()

        # Message Label
        self.message_label = QLabel(message, self)

        # Adjust width based on text length
        label_width = self.message_label.fontMetrics().boundingRect(self.message_label.text()).width()
        self.message_label.setFixedWidth(label_width + 20)  # Adding some extra space

        self.message_label.setStyleSheet(f"font-size: 13px; padding: 6px; border-radius: 10px; background-color: {'lightblue' if is_active_user else 'lightgray'}")
        self.message_label.setAlignment(QtCore.Qt.AlignRight if is_active_user else QtCore.Qt.AlignLeft)

        # Date Time Label
        self.datetime_label = QLabel(datetime, self)
        self.datetime_label.setStyleSheet("font-style: italic; font-size: 11px;")  # Date time styling
        self.datetime_label.setAlignment(QtCore.Qt.AlignLeft if not is_active_user else QtCore.Qt.AlignRight)

        # Add widgets to message group layout
        message_group_layout.addWidget(self.message_label, alignment=QtCore.Qt.AlignRight if is_active_user else QtCore.Qt.AlignLeft)
        message_group_layout.addWidget(self.datetime_label)

        # Main Layout
        main_layout = QHBoxLayout(self)

        if is_active_user:
            main_layout.addLayout(message_group_layout)
            main_layout.addWidget(self.avatar_label)
        else:
            main_layout.addWidget(self.avatar_label)
            main_layout.addLayout(message_group_layout)

        main_layout.setContentsMargins(5, 5, 5, 5)


class MessageItemWidget(QWidget):
    def __init__(self, avatar_path, username, message_preview, unread_count):
        super(MessageItemWidget, self).__init__()

        # Avatar
        self.avatar_label = QLabel(self)
        self.avatar_label.setPixmap(QtGui.QPixmap(avatar_path).scaledToWidth(50).scaledToHeight(50, QtCore.Qt.SmoothTransformation))
        self.avatar_label.setFixedSize(50, 50)
        self.avatar_label.setScaledContents(True)
        self.avatar_label.setStyleSheet("border-radius: 25px; overflow: hidden;")  # Apply rounded clipping mask

        # User Info
        user_info_layout = QVBoxLayout()
        user_info_layout.setAlignment(QtCore.Qt.AlignTop)  # Align to the top
        user_info_layout.setSpacing(5)  # Set spacing between items

        # Username Group
        username_group_layout = QHBoxLayout()
        self.username_label = QLabel(username, self)
        self.username_label.setStyleSheet("font-weight: bold;")  # Make username bold
        username_group_layout.addWidget(self.username_label)
        user_info_layout.addLayout(username_group_layout)

        # User Info Group
        user_info_group_layout = QHBoxLayout()
        self.message_preview_label = QLabel(message_preview, self)
        font = self.message_preview_label.font()
        font.setItalic(True)
        self.message_preview_label.setFont(font)

        self.unread_count_label = QLabel(unread_count, self)

        # Set styles for message preview label
        self.message_preview_label.setStyleSheet("padding: 5px;")  # Adjust styling as needed

        # Set styles for unread count label
        self.unread_count_label.setStyleSheet("background-color: lightcoral; border-radius: 10px; padding: 2px; font-weight: bold;")

        user_info_group_layout.addWidget(self.message_preview_label)
        user_info_group_layout.addStretch()  # Add stretch to push unread_count_label to the right
        user_info_group_layout.addWidget(self.unread_count_label)

        user_info_layout.addLayout(user_info_group_layout)

        # Main Layout
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.avatar_label)
        main_layout.addLayout(user_info_layout)
        main_layout.setContentsMargins(10, 10, 10, 10)

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
        #self.messageListWidget = QListWidget(self.ongoing_messages_widget)
        self.messageListWidget.setGeometry(QtCore.QRect(0, 80, 320, 551))

        # Add messages to the list inside the "Messages" tab
        self.addMessage("Use Case Diagram.png", "Ahmet", "How are you?", "2")
        self.addMessage("Use Case Diagram.png", "Mehmet", "Meeting at 2 PM", "1")
        self.addMessage("Use Case Diagram.png", "Group-1", "Discussion on project updates", "4")
        self.addMessage("Use Case Diagram.png", "Hasan", "Check the new document", "2")
        self.addMessage("Use Case Diagram.png", "Ayse", "Don't forget about the deadline", "0")
        self.addMessage("Use Case Diagram.png", "Zeynep", "Review the latest code changes", "0")

        # Add selected messages
        self.addselectedmessage("Use Case Diagram.png", "John", "Hey, how's it going?","10:00 AM", True)
        self.addselectedmessage("Use Case Diagram.png", "Alice", "Discussing project updates","10:00 AM", False)
        self.addselectedmessage("Use Case Diagram.png", "Michael", "Reviewing the latest code changes","10:00 AM", True)
        self.addselectedmessage("Use Case Diagram.png", "Emily", "Reminder: Team meeting at 3 PM","10:00 AM", True)
        self.addselectedmessage("Use Case Diagram.png", "David", "Need your feedback on the proposal","10:00 AM", False)
        self.addselectedmessage("Use Case Diagram.png", "Sophia", "Sending you the latest design drafts","10:00 AM", True)
        self.addselectedmessage("Use Case Diagram.png", "Daniel", "Quick check-in on project status","10:00 AM", True)
        self.addselectedmessage("Use Case Diagram.png", "Olivia", "Discussing upcoming deadlines","10:00 AM", False)
        self.addselectedmessage("Use Case Diagram.png", "Liam", "Reminder: Submit your weekly reports","10:00 AM", True)
        self.addselectedmessage("Use Case Diagram.png", "Emma", "Important: Client meeting tomorrow","10:00 AM", False)


         # Add users to the list
        self.addUser({"avatar_path": "path_to_avatar1.png", "username": "User 1", "user_type": "Admin"})
        self.addUser({"avatar_path": "path_to_avatar2.png", "username": "User 2", "user_type": "Regular User"})

        # Connect textChanged signal to filterUsers method
        self.user_search.setPlaceholderText("Search Users")
        self.user_search.textChanged.connect(self.filterUsers)

    def addselectedmessage(self, avatar_path, username, message_preview, time, is_active_user):
        selected_message_item = SelectedMessageItemWidget(avatar_path, username, message_preview, time, is_active_user)
        selectedListWidgetItem = QListWidgetItem(self.selectedMessageList)  # Use selectedMessageList
        selectedListWidgetItem.setSizeHint(selected_message_item.sizeHint())
        self.selectedMessageList.addItem(selectedListWidgetItem)
        self.selectedMessageList.setItemWidget(selectedListWidgetItem, selected_message_item)

    def addMessage(self, avatar_path, username, message_preview, unread_count):
        message_item = MessageItemWidget(avatar_path, username, message_preview, unread_count)

        listWidgetItem = QListWidgetItem(self.messageListWidget)  # Use messageListWidget
        listWidgetItem.setSizeHint(message_item.sizeHint())
        self.messageListWidget.addItem(listWidgetItem)
        self.messageListWidget.setItemWidget(listWidgetItem, message_item)
    
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