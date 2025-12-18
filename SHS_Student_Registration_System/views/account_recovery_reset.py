from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QGraphicsDropShadowEffect, \
    QLineEdit, QCheckBox, QPushButton, QMessageBox, QScrollArea, QComboBox, QDateEdit, QFileDialog
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt, QRect, QDate
import os

class AccountRecoveryReset(QWidget):
    def __init__(self, main_window, controller):
        super().__init__()
        self.main_window = main_window
        self.controller = controller
        self.setWindowTitle("SHS Registration System")
        self.setFixedSize(1200, 800)
        self.setStyleSheet("background-color:rgb(50, 50, 50);")

        # --- LOGO ---
        self.logo = QLabel(self)
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "files", "Final Logo - White.png")
        pixmap = QPixmap(logo_path)
        pixmap = pixmap.scaled(150, 45, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo.setGeometry(525, 25, 150, 45)

        # --- 400x400 MAIN SHAPE (centered) ---
        self.shape_main = QWidget(self)
        self.shape_main.setGeometry(400, 200, 400, 500)
        self.shape_main.setStyleSheet(
            "background-color: rgb(60, 60, 60);"
            "border-radius: 0px;"
            "border: 1px solid rgba(200, 0, 0, 50);"
        )

        # Drop shadow
        main_shadow = QGraphicsDropShadowEffect()
        main_shadow.setBlurRadius(10)
        main_shadow.setXOffset(10)
        main_shadow.setYOffset(10)
        main_shadow.setColor(QColor(0, 0, 0, 150))
        self.shape_main.setGraphicsEffect(main_shadow)

        # Title: RECOVERY
        self.title_label = QLabel("RECOVERY", self)
        self.title_label.setGeometry(500, 225, 200, 50)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                font-family: Poppins;
                font-size: 32px;
                font-weight: bold;
            }
        """)

        # Subtitle: Enter new password
        self.subtitle_label = QLabel("Enter new password", self)
        self.subtitle_label.setGeometry(450, 300, 300, 20)
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                font-family: Poppins;
                font-size: 12px;
                font-weight: normal;
            }
        """)

        # New password label
        self.label_new_password = QLabel("New Password", self)
        self.label_new_password.setGeometry(460, 345, 100, 15)
        self.label_new_password.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                font-family: Poppins;
                font-size: 12px;
                font-weight: normal;
            }
        """)

        # New password input
        self.new_password = QLineEdit(self)
        self.new_password.setGeometry(450, 360, 300, 50)
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password.setStyleSheet("""
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
        """)

        # Confirm password label
        self.label_confirm_password = QLabel("Confirm Password", self)
        self.label_confirm_password.setGeometry(460, 425, 100, 15)
        self.label_confirm_password.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgb(234, 234, 234);
                font-family: Poppins;
                font-size: 12px;
                font-weight: normal;
            }
        """)

        # Confirm password input
        self.confirm_password = QLineEdit(self)
        self.confirm_password.setGeometry(450, 440, 300, 50)
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password.setStyleSheet("""
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
        """)

        # Primary button: RESET PASSWORD
        self.submit = QPushButton("RESET PASSWORD", self)
        self.submit.setGeometry(450, 510, 300, 50)
        self.submit.setStyleSheet("""
            QPushButton {
                background-color: rgb(193, 193, 193);
                color: rgb(50, 50, 50);
                border-radius: 0px;
                border: 1px solid rgb(132, 132, 132);
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
        """)

        # Back to Login button
        self.back = QPushButton("BACK TO LOGIN", self)
        self.back.setGeometry(450, 580, 300, 50)
        self.back.setStyleSheet("""
            QPushButton {
                background-color: rgba(60, 60, 60, 0);
                color: rgb(234, 234, 234);
                border-radius: 0px;
                border: 1px solid rgb(193, 193, 193);
                padding: 10px 12px;
                font-family: Poppins;
                font-size: 16px;
                font-weight: normal;
            }
            QPushButton:hover {
                background-color: rgb(70, 70, 70);
            }
            QPushButton:pressed {
                background-color: rgb(40, 40, 40);
            }
        """)

        # Connect buttons
        self.submit.clicked.connect(self.handle_reset)
        self.back.clicked.connect(self.handle_back)

    def handle_reset(self):
        """Handle password reset"""
        if not self.main_window.recovery_account_id:
            QMessageBox.warning(self, "Error", "No account selected.")
            return

        new_password = self.new_password.text().strip()
        confirm_password = self.confirm_password.text().strip()

        if not new_password or not confirm_password:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        if self.controller.reset_password(self.main_window.recovery_account_id, new_password):
            QMessageBox.information(self, "Success", "Password reset successfully!")
            self.main_window.recovery_account_id = None
            self.main_window.switch_view("login")
        else:
            QMessageBox.warning(self, "Error", "Failed to reset password.")

    def handle_back(self):
        """Handle back button"""
        self.main_window.switch_view("account_recovery_security")
