# views/login_page.py
# Purpose: Login page UI for user authentication. Displays username and password input fields,
# login button, account creation link, and password recovery option. This follows OOP by
# encapsulating all login-related UI widgets and their behavior in a single class.

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QGraphicsDropShadowEffect, \
    QLineEdit, QCheckBox, QPushButton, QMessageBox
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt, QRect
import os


# LoginWindow class - OOP: Encapsulates login UI widgets and authentication logic
# This is an OOP class because it groups related UI components (labels, inputs, buttons) and
# their event handlers into a cohesive unit, following encapsulation and single responsibility principles.
class LoginWindow(QWidget):
    def __init__(self, main_window, auth_controller, on_login_success):
        super().__init__()
        self.main_window = main_window
        self.auth_controller = auth_controller
        self.on_login_success = on_login_success
        self.setWindowTitle("SHS Registration System")
        self.setFixedSize(1200, 800)
        self.setStyleSheet("background-color:rgb(50, 50, 50);")

        # Widget: Logo label
        self.logo = QLabel(self)
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "files", "Final Logo - White.png")
        pixmap = QPixmap(logo_path)
        pixmap = pixmap.scaled(120, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo.setGeometry(25, 20, 120, 40)

        # Widget: Central card container - the main login card with drop shadow
        self.card = QWidget(self)
        self.card.setGeometry(400, 100, 400, 600)
        self.card.setStyleSheet(
            "background-color: rgb(60, 60, 60);"
            "border-radius: 0px;"
            "border: 1px solid rgba(200, 0, 0, 50);"
        )

        # Effect: Drop shadow for the central card to create depth
        card_shadow = QGraphicsDropShadowEffect()
        card_shadow.setBlurRadius(10)
        card_shadow.setXOffset(10)
        card_shadow.setYOffset(10)
        card_shadow.setColor(QColor(0, 0, 0, 150))
        self.card.setGraphicsEffect(card_shadow)

        base_label_style = """
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                font-family: Poppins;
            }
        """

        # Widget: Welcome label - main title text "WELCOME!"
        self.label_welcome = QLabel("WELCOME!", self)
        self.label_welcome.setGeometry(500, 125, 200, 50)
        self.label_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_welcome.setStyleSheet(
            base_label_style +
            "QLabel { font-size: 32px; font-weight: bold; font-family: Poppins;}"
        )

        # Widget: System name label - displays "SHS - Student Registration System"
        self.label_system = QLabel("SHS - Student Registration System", self)
        self.label_system.setGeometry(450, 200, 300, 25)
        self.label_system.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_system.setStyleSheet(
            base_label_style +
            "QLabel { font-size: 16px; font-weight: regular; font-family: Poppins;}"
        )

        # Widget: Subtitle label - displays "Sign-in to continue"
        self.label_subtitle = QLabel("Sign-in to continue", self)
        self.label_subtitle.setGeometry(450, 250, 300, 20)
        self.label_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_subtitle.setStyleSheet(
            base_label_style +
            "QLabel { font-size: 12px; font-weight: normal; font-family: Poppins;}"
        )

        # Widget: Username field label - label for the username input field
        self.label_username = QLabel("Username", self)
        self.label_username.setGeometry(460, 295, 100, 15)
        self.label_username.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.label_username.setStyleSheet(
            base_label_style +
            "QLabel { font-size: 12px; font-weight: normal; font-family: Poppins;}"
        )

        # Widget: Password field label - label for the password input field
        self.label_password = QLabel("Password", self)
        self.label_password.setGeometry(460, 370, 100, 15)
        self.label_password.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.label_password.setStyleSheet(
            base_label_style +
            "QLabel { font-size: 12px; font-weight: normal; font-family: Poppins;}"
        )

        # Stylesheet template for line edit widgets
        line_edit_stylesheet = """
            QLineEdit {
                background-color: rgb(50, 50, 50);
                border-radius: 0px;
                border: 1px solid rgb(132, 132, 132);
                padding: 10px 12px;
                color: rgb(234, 234, 234);
                font-family: Poppins;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid rgb(234, 234, 234);
                background-color: rgb(40, 40, 40);
            }
            QLineEdit:disabled {
                color: rgb(150, 150, 150);
                border: 1px solid rgba(120, 120, 120, 80);
                background-color: rgb(35, 35, 35);
            }
            QLineEdit::placeholder {
                color: rgb(150, 150, 150);
            }
        """

        # Widget: Username input field - text input for entering username
        self.username_input = QLineEdit(self)
        self.username_input.setGeometry(450, 310, 300, 50)
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setStyleSheet(line_edit_stylesheet)

        # Widget: Password input field - text input for entering password (masked by default)
        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(450, 385, 300, 50)
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setStyleSheet(line_edit_stylesheet)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Stylesheet template for checkbox widgets
        checkbox_stylesheet = """
            QCheckBox {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                padding: 1px 1px;
                font-family: Poppins;
                font-size: 10px;
            }
            QCheckBox::indicator {
                width: 13px;
                height: 13px;
                border-radius: 0px;
                border: 1px solid rgb(150, 150, 150);
                background-color: rgb(40, 40, 40);
            }
            QCheckBox::indicator:hover {
                border: 1px solid rgb(234, 234, 234);
            }
            QCheckBox::indicator:checked {
                background-color: rgb(234, 234, 234);
                border: 1px solid rgb(234, 234, 234);
            }
        """

        # Widget: Show password checkbox - toggles password visibility
        self.remember_checkbox = QCheckBox("Show Password", self)
        self.remember_checkbox.setGeometry(635, 445, 115, 15)
        self.remember_checkbox.setStyleSheet(checkbox_stylesheet)
        self.remember_checkbox.stateChanged.connect(self.toggle_password)

        # Stylesheet template for primary buttons
        button_stylesheet = """
            QPushButton {
                background-color: rgb(193, 193, 193);
                color: rgb(50, 50, 50);
                border-radius: 0px;
                border: rgb(132, 132, 132);
                padding: 10px 12px;
                font-family: Poppins;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgb(255, 255, 255);
            }
            QPushButton:pressed {
                background-color: rgb(175, 175, 175);
            }
            QPushButton:disabled {
                background-color: rgb(90, 90, 90);
                color: rgb(160, 160, 160);
            }
        """

        # Widget: Login button - primary action button to submit login credentials
        self.primary_button = QPushButton("LOGIN", self)
        self.primary_button.setGeometry(450, 475, 300, 50)
        self.primary_button.setStyleSheet(button_stylesheet)
        self.primary_button.clicked.connect(self.handle_login)

        # Widget: Create account button - navigates to registration form
        self.register_button = QPushButton("CREATE ACCOUNT", self)
        self.register_button.setGeometry(450, 540, 300, 50)
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(193, 193, 193, 0);
                color: rgb(234, 234, 234);
                border-radius: 0px;
                border: 1px solid rgb(193, 193, 193);
                padding: 10px 12px;
                font-family: Poppins;
                font-size: 20px;
                font-weight: regular;
            }
            QPushButton:hover {
                background-color: rgb(70, 70, 70);
            }
            QPushButton:pressed {
                background-color: rgb(175, 175, 175);
            }
            QPushButton:disabled {
                background-color: rgb(90, 90, 90);
                color: rgb(160, 160, 160);
            }
        """)
        self.register_button.clicked.connect(self.handle_register)

        # Widget: Forgot password button - navigates to account recovery flow
        self.forgot_button = QPushButton("Forgot Password?", self)
        self.forgot_button.setGeometry(525, 604, 150, 20)
        self.forgot_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(193, 193, 193, 0);
                color: rgb(234, 234, 234);
                border-radius: 0px;
                border: 1px solid rgba(193, 193, 193, 0);
                padding: 1px 1px;
                font-family: Poppins;
                font-size: 12px;
                font-weight: regular;
            }
            QPushButton:hover {
                background-color: rgb(70, 70, 70);
            }
            QPushButton:pressed {
                background-color: rgb(50, 50, 50);
            }
            QPushButton:disabled {
                background-color: rgb(90, 90, 90);
                color: rgb(160, 160, 160);
            }
        """)
        self.forgot_button.clicked.connect(self.handle_forgot_password)

        # Connect Enter key press to trigger login action
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)

    # Method: Toggle password visibility based on checkbox state
    def toggle_password(self, state):
        if state == Qt.CheckState.Checked.value:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    # Method: Handle login button click - validates credentials and authenticates user
    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter both username and password.")
            return

        try:
            result = self.auth_controller.login(username, password)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Database connection error: {e}")
            return

        if result.get("success"):
            if self.on_login_success:
                self.on_login_success(result)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials. Please try again.")

    # Method: Handle create account button click - navigates to registration form
    def handle_register(self):
        self.main_window.switch_view("registration")

    # Method: Handle forgot password button click - navigates to account recovery
    def handle_forgot_password(self):
        self.main_window.switch_view("account_recovery")