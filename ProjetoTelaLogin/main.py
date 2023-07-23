import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QStackedWidget
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

# Importa a classe DataBase ou qualquer outra classe que você esteja usando para gerenciar os dados dos usuários
from database import DataBase

class CustomLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("background-color: #c3c3c3; color: #1f1f1f;")

class CreateAccountWindow(QWidget):
    def __init__(self, database, login_window):
        super().__init__()
        self.database = database
        self.login_window = login_window
        self.namee = CustomLineEdit()
        self.email = CustomLineEdit()
        self.password = CustomLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.submit_button = QPushButton("Cadastrar")
        self.submit_button.clicked.connect(self.submit)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Criar uma Conta", styleSheet="color: #b4b4b4; font-weight: bold; font-size: 14pt;"))
        layout.addWidget(QLabel("Nome:", styleSheet="color: #b4b4b4; font-size: 11pt;"))
        layout.addWidget(self.namee)
        layout.addWidget(QLabel("Email:", styleSheet="color: #b4b4b4; font-size: 11pt;"))
        layout.addWidget(self.email)
        layout.addWidget(QLabel("Senha:", styleSheet="color: #b4b4b4; font-size: 11pt;"))
        layout.addWidget(self.password)
        layout.addWidget(QLabel(""))
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def submit(self):
        name = self.namee.text()
        email = self.email.text()
        password = self.password.text()

        # Verifica se os campos estão preenchidos
        if name and email and password:
            # Valida o formato do email 
            if "@" in email and "." in email:
                # Valida a senha
                if len(password) >= 6:
                    result = database.add_user(email, password, name)
                    if result == 1:
                        # Mostra menssagem de sucesso
                        QMessageBox.information(self, "Sucesso", "Conta criada com sucesso!", QMessageBox.StandardButton.Ok)
                        self.reset()
                    
                    # Ir para a tela de login após o cadastro
                    window_manager.setCurrentIndex(0)

                    # Redefina os campos após a criação da conta
                    self.reset()
                    # Transite para a tela de login após a criação da conta
                    window_manager.setCurrentIndex(0)
                else:
                    QMessageBox.critical(self, "Erro de Cadastro", "A senha deve ter pelo menos 6 caracteres.", QMessageBox.StandardButton.Ok)
            else:
                QMessageBox.critical(self, "Erro de Cadastro", "Insira um email válido.", QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.critical(self, "Erro de Cadastro", "Preencha todos os campos com informações válidas.", QMessageBox.StandardButton.Ok)


    def reset(self):
        self.namee.setText("")
        self.email.setText("")
        self.password.setText("")

class LoginWindow(QWidget):
    def __init__(self, database, create_account_window, main_window):
        super().__init__()

        self.database = database
        self.create_account_window = create_account_window
        self.main_window = main_window
        self.email = CustomLineEdit()
        self.password = CustomLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self.loginBtn)

        self.create_account_button = QPushButton("Cadastrar")
        self.create_account_button.clicked.connect(self.show_create_account)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Email:", styleSheet="color: #b4b4b4; font-size: 11pt;"))
        layout.addWidget(self.email)
        layout.addWidget(QLabel("Senha:", styleSheet="color: #b4b4b4; font-size: 11pt;"))
        layout.addWidget(self.password)
        layout.addWidget(QLabel(""))
        layout.addWidget(self.login_button)
        layout.addWidget(self.create_account_button)
        self.setLayout(layout)

    def loginBtn(self):
        email = self.email.text()
        password = self.password.text()

        # Validacao de login

        if  database.validate_user(email, password):  # Usar o método validate_user da classe DataBase
            main_window.set_success_message("Você fez login com sucesso")
            window_manager.setCurrentIndex(2)  # Transite para a tela principal após o login
        else:
            QMessageBox.critical(self, "Erro de Login", "Nome de usuário ou senha inválidos.", QMessageBox.StandardButton.Ok)

    def show_create_account(self):
        #Transita para a tela de criar conta
        window_manager.setCurrentIndex(1)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.n = QLabel()
        self.email = QLabel()
        self.created = QLabel()

        self.logout_button = QPushButton("Sair")
        self.logout_button.clicked.connect(self.logOut)

        self.success_label = QLabel()
        self.success_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.success_label.setStyleSheet("font-size: 14pt; font-weight:bold; color: white;")

        self.error_label = QLabel()
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setStyleSheet("font-size: 14pt; font-weight:bold; color: white;")

        layout = QVBoxLayout()
        layout.addWidget(self.success_label)
        layout.addWidget(self.error_label)
        layout.addWidget(self.n)
        layout.addWidget(self.email)
        layout.addWidget(self.created)
        layout.addWidget(QLabel(""))
        layout.addWidget(self.logout_button)
        self.setLayout(layout)

    def logOut(self):
        # Faça o processamento para fazer logout aqui
        # Substitua esta parte pelo código para fazer logout
        window_manager.setCurrentIndex(0)  # Transite para a tela de login após o logout
        
        #Reseta os campos da tela de login
        login_window.password.setText("")
    
    def set_success_message(self, message):
        main_window.success_label.setText(message)

# Inicialização da aplicação
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Inicialize a classe DataBase
    database = DataBase()

    # Inicialize as janelas/telas e adicione-as ao window_manager
    main_window = MainWindow()  
    login_window = LoginWindow(database, create_account_window=None, main_window=None)
    create_account_window = CreateAccountWindow(database, login_window)  # Passe a instância da classe DataBase aqui
    window_manager = QStackedWidget()
    window_manager.addWidget(login_window)
    window_manager.addWidget(create_account_window)
    window_manager.addWidget(main_window)

    # Defina a janela/tela inicial como a tela de login
    window_manager.setCurrentIndex(0)

    window_manager.show()
    sys.exit(app.exec())

