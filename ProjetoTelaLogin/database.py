import sys
import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QStackedWidget

class DataBase:
    def __init__(self):
        self.users = {}
        self.load()

    def load(self):
    # Alguns usuários de teste apenas para fins de demonstração
        self.users["login1@email.com"] = {
            "password": "password1", 
            "name": "Test User 1", 
            "created": DataBase.get_date()
        }  
        self.users["login2@email.com"] = {
            "password": "password2", 
            "name": "Test User 2", 
            "created": DataBase.get_date()
        }  
        pass

    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return None

    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            self.users[email.strip()] = {
                "password": password.strip(), 
                "name": name.strip(), 
                "created": DataBase.get_date()
            } 
            return 1
        else:
            print("Email exists already")
            return -1

    def validate_user(self, email, password):
        user = self.get_user(email)
        if user and user["password"] == password:
            return True
        return False

    """def save(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(user + ";" + self.users[user][0] + ";" + self.users[user][1] + ";" + self.users[user][2] + "\n")"""

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]

    